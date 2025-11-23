import FreeCAD

FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Cargando núcleo...\n")

def Initialize():
    FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Inicializado correctamente.\n")

def GetClassName():
    return "PythonWorkbench"
