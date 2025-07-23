import json
import os
from typing import Any

def save_gamestate(state_json: dict[Any, Any], filename: str = "gamestate.json"):
    with open(filename, "w", encoding="utf-8") as f:
        #json.dump(state_json, f, default= lambda o: o.to_json())
        json.dump(state_json, f, indent=4, default= lambda o: o.to_json())

def load_gamestate(filename: str = "gamestate.json") -> dict[str, Any]:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
    
def delete_save(filename: str = "gamestate.json") -> None:
    try:
        os.remove(filename)
        print(f"Sauvegarde '{filename}' supprimée.")
    except FileNotFoundError:
        print(f"Aucune sauvegarde '{filename}' à supprimer.")