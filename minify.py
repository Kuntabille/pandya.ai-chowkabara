import json
with open('canvas.json') as f:
    data = json.load(f)
with open('canvas.min.json', 'w') as f:
    json.dump(data, f, separators=(',', ':'))
