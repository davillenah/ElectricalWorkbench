

# ./Utils/db_manager.py

"""
DB Manager ligero para ElectricalWorkbench.

Provee operaciones CRUD atómicas para:
  - clients.json
  - projects.json

Características:
 - Uso de CUIT/CUIL como ID de cliente cuando exista.
 - Escritura atómica (tmp + os.replace).
 - API en forma de clase DBManager para fácil reutilización.
 - Logs con Utils.logger.
"""

import os
import json
import uuid
import datetime
from typing import Optional, Dict, List

from Utils.paths import get_clients_db_path, get_projects_db_path, _ensure_json_exists
from Utils.logger import log_info, log_error

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def _atomic_write(path: str, data: dict) -> bool:
    """
    Escritura atómica: guarda en path + '.tmp' y luego renombra con os.replace.
    Retorna True si se completó correctamente.
    """
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(tmp, path)
        return True
    except Exception as e:
        log_error("./Utils", "db_manager.py", f"Error guardando {path}: {e}")
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass
        return False

# ---------------------------------------------------------------------------
# DBManager (OOP)
# ---------------------------------------------------------------------------

class DBManager:
    """
    Clase responsable de leer/escribir los archivos de datos locales.
    Crear una instancia y reutilizarla.
    """

    def __init__(self):
        # Rutas relativas según DEV_MODE y paths
        self.clients_path = get_clients_db_path()
        self.projects_path = get_projects_db_path()

        # Asegurar archivos con estructura mínima
        _ensure_json_exists(self.clients_path, {"clients": []})
        _ensure_json_exists(self.projects_path, {"projects": [], "current_project_id": None})

    # -------------------------
    # CLIENTS
    # -------------------------
    def load_clients(self) -> List[Dict]:
        """Carga y retorna la lista de clientes."""
        try:
            with open(self.clients_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("clients", [])
        except Exception as e:
            log_error("./Utils", "db_manager.py", f"load_clients error: {e}")
            return []

    def save_clients(self, clients: List[Dict]) -> bool:
        """Guarda la lista completa de clientes (atómico)."""
        data = {"clients": clients}
        ok = _atomic_write(self.clients_path, data)
        if ok:
            log_info("./Utils", "db_manager.py", f"clients.json actualizado ({len(clients)} clientes).")
        return ok

    def find_client_by_cuit(self, cuit: str) -> Optional[Dict]:
        """Busca un cliente por CUIT/CUIL y retorna el dict o None."""
        if not cuit:
            return None
        clients = self.load_clients()
        for c in clients:
            if c.get("cuit") and str(c.get("cuit")) == str(cuit):
                return c
        return None

    def add_or_update_client(self, client: Dict) -> Dict:
        """
        Añade o actualiza un cliente.
        Campos recomendados:
          { "name", "cuit", "address", "contact_name", "contact_email", "contact_phone" }
        Retorna el cliente guardado (tiene id, created_at, updated_at).
        """
        clients = self.load_clients()

        cuit = client.get("cuit") or client.get("Cuit") or None

        if cuit:
            existing = next((c for c in clients if c.get("cuit") and str(c.get("cuit")) == str(cuit)), None)
        else:
            existing = None

        if existing:
            # actualizar campos relevantes y updated_at
            existing.update({
                "name": client.get("name", existing.get("name")),
                "address": client.get("address", existing.get("address")),
                "contact_name": client.get("contact_name", existing.get("contact_name")),
                "contact_email": client.get("contact_email", existing.get("contact_email")),
                "contact_phone": client.get("contact_phone", existing.get("contact_phone")),
                "updated_at": _now_iso()
            })
            saved = existing
            action = "actualizado"
        else:
            new_id = str(cuit) if cuit else str(uuid.uuid4())
            saved = {
                "id": new_id,
                "name": client.get("name", ""),
                "cuit": cuit or "",
                "address": client.get("address", ""),
                "contact_name": client.get("contact_name", ""),
                "contact_email": client.get("contact_email", ""),
                "contact_phone": client.get("contact_phone", ""),
                "created_at": _now_iso(),
                "updated_at": _now_iso()
            }
            clients.append(saved)
            action = "creado"

        if self.save_clients(clients):
            log_info("./Utils", "db_manager.py", f"Cliente {action}: {saved.get('name')}")
        else:
            log_error("./Utils", "db_manager.py", "No se pudo persistir clients.json")

        return saved

    # -------------------------
    # PROJECTS
    # -------------------------
    def load_projects_data(self) -> Dict:
        """Carga el objeto completo de projects.json."""
        try:
            with open(self.projects_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            log_error("./Utils", "db_manager.py", f"load_projects_data error: {e}")
            return {"projects": [], "current_project_id": None}

    def save_projects_data(self, data: Dict) -> bool:
        """Guarda el objeto completo de projects.json de forma atómica."""
        ok = _atomic_write(self.projects_path, data)
        if ok:
            log_info("./Utils", "db_manager.py", "projects.json actualizado.")
        return ok

    def load_projects(self) -> List[Dict]:
        """Retorna la lista de proyectos."""
        data = self.load_projects_data()
        return data.get("projects", [])

    def find_project_by_id(self, project_id: str) -> Optional[Dict]:
        if not project_id:
            return None
        projects = self.load_projects()
        for p in projects:
            if p.get("id") == project_id:
                return p
        return None

    def add_or_update_project(self, project: Dict, mark_current: bool = True) -> Dict:
        """
        Añade o actualiza un proyecto. Campos recomendados:
          { "name", "code", "path", "template", "type", "purpose", "client_id", "status", "version", "is_macro" }
        - Si no viene 'id' se genera uuid.
        - Si mark_current=True, marca el proyecto como current.
        Retorna el proyecto guardado.
        """
        data = self.load_projects_data()
        projects = data.get("projects", [])

        proj_id = project.get("id")
        existing = None
        if proj_id:
            existing = next((p for p in projects if p.get("id") == proj_id), None)
        else:
            path = project.get("path")
            if path:
                existing = next((p for p in projects if p.get("path") == path), None)

        if existing:
            existing.update({
                "name": project.get("name", existing.get("name")),
                "code": project.get("code", existing.get("code")),
                "path": project.get("path", existing.get("path")),
                "template": project.get("template", existing.get("template")),
                "type": project.get("type", existing.get("type")),
                "purpose": project.get("purpose", existing.get("purpose")),
                "client_id": project.get("client_id", existing.get("client_id")),
                "status": project.get("status", existing.get("status")),
                "version": project.get("version", existing.get("version")),
                "is_macro": project.get("is_macro", existing.get("is_macro", False)),
                "updated_at": _now_iso()
            })
            saved = existing
            action = "actualizado"
        else:
            new_id = str(uuid.uuid4())
            saved = {
                "id": new_id,
                "name": project.get("name", ""),
                "code": project.get("code", ""),
                "path": project.get("path", ""),
                "template": project.get("template", ""),
                "type": project.get("type", ""),
                "purpose": project.get("purpose", ""),
                "client_id": project.get("client_id", ""),
                "status": project.get("status", "En proceso"),
                "version": project.get("version", "0.1.0"),
                "is_macro": project.get("is_macro", False),
                "created_at": _now_iso(),
                "updated_at": _now_iso()
            }
            projects.append(saved)
            action = "creado"

        data["projects"] = projects
        if mark_current:
            data["current_project_id"] = saved.get("id")

        if self.save_projects_data(data):
            log_info("./Utils", "db_manager.py", f"Proyecto {action}: {saved.get('name')} (id={saved.get('id')})")
        else:
            log_error("./Utils", "db_manager.py", "No se pudo persistir projects.json")

        return saved

    def set_current_project(self, project_id: Optional[str]) -> bool:
        """
        Marca el proyecto por id como current. Si project_id es None lo desmarca.
        """
        data = self.load_projects_data()
        data["current_project_id"] = project_id
        return self.save_projects_data(data)

    def get_current_project(self) -> Optional[Dict]:
        """
        Retorna el project dict seleccionado actualmente, o None si no hay.
        """
        data = self.load_projects_data()
        current_id = data.get("current_project_id")
        if not current_id:
            return None
        return self.find_project_by_id(current_id)

    # -------------------------
    # UTILIDADES
    # -------------------------
    def remove_project(self, project_id: str) -> bool:
        """
        Elimina un proyecto por id (no borra archivos en disco).
        Si era current_project_id lo desmarca.
        """
        data = self.load_projects_data()
        projects = data.get("projects", [])
        new_list = [p for p in projects if p.get("id") != project_id]
        data["projects"] = new_list
        if data.get("current_project_id") == project_id:
            data["current_project_id"] = None
        return self.save_projects_data(data)

    def remove_client(self, client_id_or_cuit: str) -> bool:
        """
        Elimina un cliente por id o por cuit.
        """
        clients = self.load_clients()
        new_list = [c for c in clients if not (c.get("id") == client_id_or_cuit or c.get("cuit") == client_id_or_cuit)]
        return self.save_clients(new_list)
