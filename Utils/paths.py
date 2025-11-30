

# ./Utils/paths.py

"""
Utils.paths
Rutas y utilidades relacionadas con paths y archivos de configuración/BD local.

Reglas:
 - En DEV_MODE=True los JSON y datos se guardan dentro del workbench (.data/) para pruebas rápidas.
 - En DEV_MODE=False los JSON se guardan en FreeCAD.getUserAppDataDir()/ElectricalWorkbench/.
 - get_project_path() lee projects.json y devuelve la ruta del proyecto marcado como actual.
"""

import os
import json
import FreeCAD

from Utils.config import DEV_MODE

def get_workbench_path() -> str:
    """
    Ruta absoluta al directorio raíz del workbench.
    Ej: /home/user/.local/share/FreeCAD/Mod/ElectricalWorkbench
    """
    return os.path.dirname(os.path.dirname(__file__))


def get_icon_path(icon_name: str) -> str:
    """
    Ruta absoluta a iconos dentro del workbench.
    """
    return os.path.join(get_workbench_path(), "resources", "icons", icon_name)


def get_user_app_dir() -> str:
    """
    Carpeta de datos del usuario facilitada por FreeCAD.
    /home/user/.FreeCAD (según FreeCAD.getUserAppDataDir()) + ElectricalWorkbench
    """
    base = FreeCAD.getUserAppDataDir()
    app_dir = os.path.join(base, "ElectricalWorkbench")
    os.makedirs(app_dir, exist_ok=True)
    return app_dir


def get_workbench_data_dir() -> str:
    """
    Carpeta de datos dentro del propio workbench para pruebas (DEV).
    /.../Mod/ElectricalWorkbench/.data
    """
    wb = get_workbench_path()
    data_dir = os.path.join(wb, ".data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_user_db_dir() -> str:
    """
    Devuelve la carpeta donde guardamos los JSON de la 'DB' local.
    - DEV_MODE True: dentro del workbench (.data) para pruebas
    - DEV_MODE False: en FreeCAD user app dir
    """
    if DEV_MODE:
        return get_workbench_data_dir()
    else:
        return get_user_app_dir()


def get_clients_db_path(filename: str = "clients.json") -> str:
    """
    Ruta completa al archivo clients.json en la carpeta de datos del usuario/workbench.
    """
    return os.path.join(get_user_db_dir(), filename)


def get_projects_db_path(filename: str = "projects.json") -> str:
    """
    Ruta completa al archivo projects.json en la carpeta de datos del usuario/workbench.
    """
    return os.path.join(get_user_db_dir(), filename)


def get_config_path(file_name: str = "config.json") -> str:
    """
    Ruta general de configuración (compatibilidad con implementaciones previas).
    """
    user_data_path = get_user_app_dir()
    return os.path.join(user_data_path, file_name)


def _ensure_json_exists(path: str, fallback: dict):
    """
    Helper interno: si el JSON no existe lo crea con 'fallback'.
    No lanza excepción si falla: quien llame debe manejar el fallo si es crítico.
    """
    if not os.path.exists(path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(fallback, f, indent=4, ensure_ascii=False)
        except Exception:
            pass


def get_project_path() -> str | None:
    """
    Devuelve la ruta del proyecto actualmente marcado como 'current' en projects.json.

    Flujo:
      - Lee projects.json (si no existe, devuelve None)
      - Si existe 'current_project_id', busca el proyecto y devuelve su 'path'
      - Si no hay current_project_id, devuelve None
    """
    projects_file = get_projects_db_path()
    _ensure_json_exists(projects_file, {"projects": [], "current_project_id": None})

    try:
        with open(projects_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None

    current_id = data.get("current_project_id")
    if not current_id:
        return None

    for proj in data.get("projects", []):
        if proj.get("id") == current_id:
            return proj.get("path")
    return None
