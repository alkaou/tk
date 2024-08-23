import os
import json

class JsonManager:

    @staticmethod
    def write_json(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_json_file(file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                pass  # Continue si le fichier est mal formaté
        # Retourne un dictionnaire par défaut si le fichier n'existe pas ou est vide/mal formaté
        return {
            "vocab": {
                "": 0, 
                "<|start_word|>": 1,
                "<|end_word|>": 2,
                "<|start_phrase|>": 3,
                "<|end_phrase|>": 4,
            }
        }
