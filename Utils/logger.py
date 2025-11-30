

# ./Utils/logger.py

import FreeCAD
from Utils.config import DEV_MODE

def _write(msg: str):
    FreeCAD.Console.PrintMessage(msg + "\n")

def _write_error(msg: str):
    FreeCAD.Console.PrintError(msg + "\n")


def log_info(module: str, file: str, message: str):
    """
    Log informativo estándar.
    """
    if DEV_MODE:
        try:
            _write(f"[EW]-[{module}/{file}] → {message}")
        except Exception:
            print(f"[EW]-[{module}/{file}] → {message}")


def log_error(module: str, file: str, error: str):
    """
    Log de error estándar.
    """
    if DEV_MODE:
        try:
            _write_error(f"[EW]-[{module}/{file}] → {error}")
        except Exception:
            print(f"[EW]-[{module}/{file}] → {error}")