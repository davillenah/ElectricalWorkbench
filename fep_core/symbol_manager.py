import os, json
import FreeCAD

class SymbolManager:
    def __init__(self, base_path):
        self.base_path = base_path

    def list_symbols(self):
        return [
            f.replace(".json","")
            for f in os.listdir(self.base_path)
            if f.endswith(".json")
        ]

    def load_symbol(self, name):
        json_path = os.path.join(self.base_path, name + ".json")
        svg_path = os.path.join(self.base_path, name + ".svg")

        if not os.path.exists(json_path):
            raise FileNotFoundError("Metadata JSON no encontrado: " + json_path)

        if not os.path.exists(svg_path):
            raise FileNotFoundError("SVG no encontrado: " + svg_path)

        with open(json_path, "r") as f:
            data = json.load(f)

        data["svg"] = svg_path
        return data
