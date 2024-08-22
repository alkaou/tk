import os
import json

class Json:

    @staticmethod
    def write_json(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_json_file(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding="utf-8") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}  # Retourne un dictionnaire vide si le fichier est vide ou mal formaté
        else:
            return {
                "vocab": {
                    "": 0, 
                    "<|start_word|>": 1,
                    "<|end_word|>": 2,
                    "<|start_phrase|>": 3,
                    "<|end_phrase|>": 4,
                }
            }