import json
from pathlib import Path

SCRIPTS_ROUTE = Path(__file__).parent
JSON_ROUTE = SCRIPTS_ROUTE / "data.json"
try:
    with open(JSON_ROUTE, "r", encoding="utf-8") as archiver:
        data = json.load(archiver)

    with open(JSON_ROUTE, "w", encoding="utf-8") as archivew:
        new_data = {"dirección": "Gotham", "ocupación": "Batman"}
        data.update(new_data)
        json.dump(data, archivew, indent=4, ensure_ascii=False)

except FileNotFoundError:
    print("No se encontró el archivo.")
except json.JSONDecodeError:
    print("El archivo no es válido.")
