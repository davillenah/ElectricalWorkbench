

# ./InitGui.py

from Utils.logger import log_info, log_error
from workbench import ElectricalWorkbenchClass

log_info(".", "InitGui.py", "Cargando GUI...")

class ElectricalWorkbench(ElectricalWorkbenchClass):
    pass

FreeCADGui.addWorkbench(ElectricalWorkbench())