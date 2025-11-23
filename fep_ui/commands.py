import FreeCAD, FreeCADGui

def register_all_commands():
    FreeCADGui.addCommand("FEP_OpenSymbolManager", OpenSymbolManager())

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
