import FreeCAD

class FEPCore:
    def __init__(self):
        self.initialized = False

    def initialize(self):
        if self.initialized:
            return
        FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Inicializando núcleo...\n")
        self.initialized = True
        return True
