import FreeCAD
import os, zipfile

class ReleaseManager:
    def __init__(self, mod_path):
        self.mod_path = mod_path

    def create_release(self, project_path, output_zip):
        FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Empaquetando proyecto...\n")
        with zipfile.ZipFile(output_zip, 'w') as z:
            for root, dirs, files in os.walk(project_path):
                for f in files:
                    fullpath = os.path.join(root, f)
                    rel = os.path.relpath(fullpath, project_path)
                    z.write(fullpath, rel)
        FreeCAD.Console.PrintMessage("[ElectricalWorkbench] Release generado: " + output_zip + "\n")
