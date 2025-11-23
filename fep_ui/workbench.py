import FreeCADGui
from fep_ui.commands import register_all_commands

class ElectricalWorkbenchClass(FreeCADGui.Workbench):
    MenuText = "Electrical"
    ToolTip = "Electrical Workbench"
    Icon = "resources/icons/FEP_icon.svg"

    def Initialize(self):
        register_all_commands()
        self.appendMenu("FEP Tools", ["FEP_OpenSymbolManager"])
        self.appendToolbar("FEP Tools", ["FEP_OpenSymbolManager"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"
