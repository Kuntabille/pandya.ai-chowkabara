import json

with open('canvas.json', 'r') as f:
    data = json.load(f)

for v in data.get('variations', []):
    if 'board' in v:
        v['boardConfigOverride'] = v.pop('board')

with open('canvas.json', 'w') as f:
    json.dump(data, f)
