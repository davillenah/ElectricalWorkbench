

# ./Utils/config.py

"""
Utils/config.py

Configuración central del Workbench Electrical.

Provee:
  - DEV_MODE: flag global para logs/diagnóstico (True en desarrollo).
  - Config: objeto compatible para importaciones que esperan 'Config'.
  - save_setting / get_setting: helpers ligeros para persistir parámetros
    usando FreeCAD.ParamGet cuando FreeCAD está disponible.
  
Comentarios en español y diseño para compatibilidad retroactiva.
"""

from types import SimpleNamespace
import os

# Intentamos importar FreeCAD sólo si estamos ejecutando dentro de FreeCAD.
# Si no está, exponemos una API mínima para evitar que el módulo falle
# en entornos de test o linters.
try:
    import FreeCAD
    _HAS_FREECAD = True
except Exception:
    FreeCAD = None
    _HAS_FREECAD = False

# -----------------------
# CONFIGURACIÓN GLOBAL
# -----------------------

# True -> modo desarrollo (imprime logs en consola de FreeCAD si está presente)
# False -> modo producción (silencioso)
DEV_MODE = True

# Objeto 'Config' para compatibilidad con código que importa: from Utils.config import Config
# Contiene los parámetros básicos y puede extenderse en el futuro.
Config = SimpleNamespace(
    DEV_MODE=DEV_MODE,
    USER_APP_DIR=(FreeCAD.getUserAppDataDir() if _HAS_FREECAD else os.path.expanduser("~/.local/share/FreeCAD")),
    # puedes añadir aquí otras opciones globales si lo necesitas
)

# -----------------------
# HELPERS DE PERSISTENCIA
# -----------------------

def save_setting(group: str, key: str, value):
    """
    Guarda una configuración usando FreeCAD.ParamGet cuando FreeCAD está disponible.
    group/key son concatenados para organización interna.
    Si FreeCAD no está disponible, intenta guardar en un archivo JSON en el user app dir.
    """
    try:
        if _HAS_FREECAD:
            param = FreeCAD.ParamGet("User parameter:Plugins/ElectricalWorkbench")
            param.SetString(f"{group}/{key}", str(value))
            return True
        else:
            # fallback simple: guardar en archivo de texto (no crítico)
            fallback_dir = os.path.join(Config.USER_APP_DIR, "ElectricalWorkbench")
            os.makedirs(fallback_dir, exist_ok=True)
            # archivo por grupo
            file_path = os.path.join(fallback_dir, f"{group}.cfg")
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"{key}={value}\n")
            return True
    except Exception as e:
        # No usar log_error aquí para evitar import ciclo; imprimir simple si DEV_MODE.
        if DEV_MODE:
            try:
                FreeCAD.Console.PrintError(f"[Utils.config] Error save_setting: {e}\n")
            except Exception:
                print(f"[Utils.config] Error save_setting: {e}")
        return False


def get_setting(group: str, key: str, default=None):
    """
    Recupera una configuración. Primero intenta ParamGet (FreeCAD). Si falla,
    intenta lectura simple del fallback file.
    """
    try:
        if _HAS_FREECAD:
            param = FreeCAD.ParamGet("User parameter:Plugins/ElectricalWorkbench")
            return param.GetString(f"{group}/{key}", default)
        else:
            # fallback: leer archivo simple si existe
            fallback_dir = os.path.join(Config.USER_APP_DIR, "ElectricalWorkbench")
            file_path = os.path.join(fallback_dir, f"{group}.cfg")
            if not os.path.isfile(file_path):
                return default
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.rstrip("\n").split("=", 1)
                            if k == key:
                                return v
                return default
            except Exception:
                return default
    except Exception as e:
        if DEV_MODE:
            try:
                FreeCAD.Console.PrintError(f"[Utils.config] Error get_setting: {e}\n")
            except Exception:
                print(f"[Utils.config] Error get_setting: {e}")
        return default


# -----------------------
# UTILIDADES ADICIONALES (opcionales)
# -----------------------

def get_user_app_dir() -> str:
    """
    Ruta base para datos del usuario. Si FreeCAD está presente usa getUserAppDataDir(),
    si no, devuelve una ruta en $HOME/.local/share/FreeCAD.
    """
    if _HAS_FREECAD:
        return FreeCAD.getUserAppDataDir()
    return Config.USER_APP_DIR


# Exponer variables útiles en el módulo
__all__ = [
    "DEV_MODE",
    "Config",
    "save_setting",
    "get_setting",
    "get_user_app_dir",
]
