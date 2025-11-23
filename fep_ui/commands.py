import FreeCAD, FreeCADGui

def register_all_commands():
    FreeCADGui.addCommand("FEP_OpenSymbolManager", OpenSymbolManager())
    FreeCADGui.addCommand("FEP_CreateProject", CreateProject())
    FreeCADGui.addCommand("FEP_GenerateRelease", GenerateRelease())
    FreeCADGui.addCommand("FEP_CloseProject", CloseProject())

# ---------------------------
#   ADMINISTRADOR DE SÍMBOLOS
# ---------------------------
class OpenSymbolManager:
    def GetResources(self):
        return {
            "MenuText": "Administrar Símbolos",
            "ToolTip": "Carga y administración de símbolos SVG+JSON",
            "Pixmap": "resources/icons/FEP_icon.svg"
        }

    def Activated(self):
        FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Symbol Manager abierto.\n")

    def IsActive(self):
        return True


# ---------------------------
#   CREAR PROYECTO
# ---------------------------
class CreateProject:
    def GetResources(self):
        return {
            "MenuText": "Crear Proyecto",
            "ToolTip": "Crea un nuevo proyecto eléctrico FEP",
            "Pixmap": "resources/icons/FEP_icon.svg"
        }

    def Activated(self):
        FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Crear Proyecto (TODO)…\n")

    def IsActive(self):
        return True


# ---------------------------
#   GENERAR RELEASE
# ---------------------------
class GenerateRelease:
    def GetResources(self):
        return {
            "MenuText": "Generar Release",
            "ToolTip": "Genera versión empaquetada del proyecto",
            "Pixmap": "resources/icons/FEP_icon.svg"
        }

    def Activated(self):
        FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Generar Release (TODO)…\n")

    def IsActive(self):
        return True


# ---------------------------
#   CERRAR PROYECTO
# ---------------------------
class CloseProject:
    def GetResources(self):
        return {
            "MenuText": "Cerrar Proyecto",
            "ToolTip": "Cierra y guarda el proyecto actual",
            "Pixmap": "resources/icons/FEP_icon.svg"
        }

    def Activated(self):
        FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Cerrar Proyecto (TODO)…\n")

    def IsActive(self):
        return True
