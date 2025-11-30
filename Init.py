

# ./Init.py

import FreeCAD
from Utils.logger import log_info, log_error

log_info(".", "Init.py", "Cargando núcleo...")

def Initialize():
    log_info(".", "Init.py", "Inicializado correctamente.")

def GetClassName():
    return "PythonWorkbench"