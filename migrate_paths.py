import json
import re

with open("logic.lua", "r") as f:
    lua_code = f.read()

# Extract 5x5 paths
p1_5x5 = re.search(r"local p1_path_5x5 = (\{.*\})", lua_code).group(1)
p2_5x5 = re.search(r"local p2_path_5x5 = (\{.*\})", lua_code).group(1)
p3_5x5 = re.search(r"local p3_path_5x5 = (\{.*\})", lua_code).group(1)
p4_5x5 = re.search(r"local p4_path_5x5 = (\{.*\})", lua_code).group(1)

# Extract 7x7 paths
p1_7x7 = re.search(r"local p1_path_7x7 = (\{.*\})", lua_code).group(1)
p2_7x7 = re.search(r"local p2_path_7x7 = (\{.*\})", lua_code).group(1)
p3_7x7 = re.search(r"local p3_path_7x7 = (\{.*\})", lua_code).group(1)
p4_7x7 = re.search(r"local p4_path_7x7 = (\{.*\})", lua_code).group(1)

def parse_lua_array(arr_str):
    arr_str = arr_str.replace("{", "[").replace("}", "]")
    arr = json.loads(arr_str)
    return [f"{x},{y}" for x, y in arr]

base_paths = [
    {"id": "p1_path", "nodes": parse_lua_array(p1_5x5)},
    {"id": "p2_path", "nodes": parse_lua_array(p2_5x5)},
    {"id": "p3_path", "nodes": parse_lua_array(p3_5x5)},
    {"id": "p4_path", "nodes": parse_lua_array(p4_5x5)},
]

var_paths = [
    {"id": "p1_path", "nodes": parse_lua_array(p1_7x7)},
    {"id": "p2_path", "nodes": parse_lua_array(p2_7x7)},
    {"id": "p3_path", "nodes": parse_lua_array(p3_7x7)},
    {"id": "p4_path", "nodes": parse_lua_array(p4_7x7)},
]

with open("canvas.json", "r") as f:
    canvas = json.load(f)

if "setup" not in canvas:
    canvas["setup"] = {}
canvas["setup"]["paths"] = base_paths

if "variations" in canvas:
    for v in canvas["variations"]:
        if v["id"] == "7x7":
            v["paths"] = var_paths

with open("canvas.json", "w") as f:
    json.dump(canvas, f, indent=2)

# Update logic.lua
new_lua = lua_code

# Remove old path definitions
new_lua = re.sub(r"local p\d_path_5x5 = \{.*?\}.*?\n", "", new_lua)
new_lua = re.sub(r"local p\d_path_7x7 = \{.*?\}.*?\n", "", new_lua)

# Update get_physical
new_get_physical = """local function get_physical(player, pos)
    if pos == 0 then return {-1, -1} end
    local p_str = "p" .. (player + 1) .. "_path"
    local node = paths.get_node(p_str, pos)
    if node then
        local x, y = string.match(node, "(%d+),(%d+)")
        return {tonumber(x), tonumber(y)}
    end
    return {-1, -1}
end"""

new_lua = re.sub(r"local function get_physical\(player, pos, variant\).*?return \{-1, -1\}\nend", new_get_physical, new_lua, flags=re.DOTALL)

# Update get_path_index
new_get_path_index = """local function get_path_index(player, x, y)
    local p_str = "p" .. (player + 1) .. "_path"
    local cell = x .. "," .. y
    local idx = paths.get_index(p_str, cell)
    if idx == 0 then return -1 end
    return idx
end"""

new_lua = re.sub(r"local function get_path_index\(player, x, y, variant\).*?return -1\nend", new_get_path_index, new_lua, flags=re.DOTALL)

# Update calls
new_lua = new_lua.replace("get_physical(i-1, 1, var)", "get_physical(i-1, 1)")
new_lua = new_lua.replace("get_path_index(opp, x, y, variant)", "get_path_index(opp, x, y)")
new_lua = new_lua.replace("get_physical(opp, 1, variant)", "get_physical(opp, 1)")
new_lua = new_lua.replace("get_path_index(player_index, x, y, var)", "get_path_index(player_index, x, y)")
new_lua = new_lua.replace("get_physical(player_index, new_idx, var)", "get_physical(player_index, new_idx)")

with open("logic.lua", "w") as f:
    f.write(new_lua)

