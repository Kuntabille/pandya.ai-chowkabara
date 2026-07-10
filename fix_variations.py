import json

with open("canvas.json", "r") as f:
    data = json.load(f)

if "variants" in data:
    del data["variants"]

data["variations"] = [
    {
        "id": "7x7",
        "name": "7x7 Board",
        "description": "Play on a larger 7x7 board with 6 pieces."
    }
]

with open("canvas.json", "w") as f:
    json.dump(data, f, indent=2)

