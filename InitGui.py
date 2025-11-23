import FreeCADGui
import FreeCAD
from fep_ui.workbench import ElectricalWorkbenchClass

FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Cargando GUI...\n")

class ElectricalWorkbench(ElectricalWorkbenchClass):
    pass

FreeCADGui.addWorkbench(ElectricalWorkbench())
