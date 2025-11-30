

# ./Commands/__init__.py

import os
import importlib
import FreeCADGui
from Utils.logger import log_error, log_info

REGISTERED_COMMANDS = []

IGNORED_FOLDERS = [
    "CommandTemplate",
    "__pycache__",
]


def register_all_commands():
    """
    Carga TODOS los comandos que cumplan con formato *_Command.py
    dentro de cada subcarpeta en Commands/.
    """

    global REGISTERED_COMMANDS

    commands_dir = os.path.dirname(__file__)

    for folder in os.listdir(commands_dir):
        folder_path = os.path.join(commands_dir, folder)

        # ---------------------------
        # IGNORAR SI NO ES CARPETA
        # ---------------------------
        if not os.path.isdir(folder_path):
            continue

        if folder in IGNORED_FOLDERS:
            continue

        if folder.startswith(".") or folder.startswith("_"):
            continue

        # ---------------------------
        # BUSCAR *_Command.py
        # ---------------------------
        command_files = [
            f for f in os.listdir(folder_path)
            if f.endswith("_Command.py")
        ]

        if not command_files:
            continue

        for file in command_files:

            module_name = file.replace(".py", "")
            import_path = f"Commands.{folder}.{module_name}"

            try:
                module = importlib.import_module(import_path)
                log_info("./Commands", "__init__.py",
                         f"[{folder}] → Cargando el módulo → {module_name}")
            except Exception as e:
                log_error("./Commands", "__init__.py",
                          f"[{folder}] → Error al importar {file} → {e}")
                continue

            # ---------------------------
            # BUSCAR CLASES DE COMANDO
            # ---------------------------
            for attr_name in dir(module):
                attr = getattr(module, attr_name)

                if (
                    isinstance(attr, type)
                    and hasattr(attr, "Activated")
                    and hasattr(attr, "GetResources")
                ):
                    command_instance = attr()
                    command_name = f"EW_{attr_name}"

                    if command_name not in REGISTERED_COMMANDS:
                        try:
                            FreeCADGui.addCommand(command_name, command_instance)
                            REGISTERED_COMMANDS.append(command_name)
                            log_info("./Commands", "__init__.py",
                                     f"[{folder}] → Comando {command_name} Registrado")
                        except Exception as e:
                            log_error("./Commands", "__init__.py",
                                      f"[{folder}] → Error registrando {command_name} → {e}")

    return REGISTERED_COMMANDS
