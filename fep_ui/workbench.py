import FreeCADGui
from fep_ui.commands import register_all_commands

class ElectricalWorkbenchClass(FreeCADGui.Workbench):
    MenuText = "Electrical"
    ToolTip = "Electrical Workbench"
    Icon = "resources/icons/FEP_icon.svg"

    def Initialize(self):
        register_all_commands()

        self.appendMenu("FEP Tools", [
            "FEP_OpenSymbolManager",
            "FEP_CreateProject",
            "FEP_GenerateRelease",
            "FEP_CloseProject"
        ])

        self.appendToolbar("FEP Tools", [
            "FEP_OpenSymbolManager",
            "FEP_CreateProject",
            "FEP_GenerateRelease",
            "FEP_CloseProject"
        ])

    def GetClassName(self):
        return "Gui::PythonWorkbench"
