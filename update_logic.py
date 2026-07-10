import re

with open("logic.lua", "r") as f:
    logic = f.read()

# Replace hardcoded arrays with a function that fetches from paths
replacement = """local function get_physical(player, pos, variant)
    if pos == 0 then return {-1, -1} end
    
    local path_id = "p" .. (player + 1) .. "_path"
    local nodes = paths.get_nodes(path_id)
    if nodes and #nodes >= pos then
        return {nodes[pos].x, nodes[pos].y}
    end
    return {-1, -1}
end

local function get_path_index(player, x, y, variant)
    local path_id = "p" .. (player + 1) .. "_path"
    local nodes = paths.get_nodes(path_id)
    if nodes then
        for i, node in ipairs(nodes) do
            if node.x == x and node.y == y then
                return i
            end
        end
    end
    return -1
end"""

# We need to replace the old get_physical and get_path_index functions.
# They are quite large, so we use regex.

logic = re.sub(r'local function get_physical\(player, pos, variant\).*?return \{-1, -1\}\nend', replacement, logic, flags=re.DOTALL)
logic = re.sub(r'local function get_path_index\(player, x, y, variant\).*?return -1\nend', '', logic, flags=re.DOTALL)

# Remove the hardcoded tables
logic = re.sub(r'local p\d_path_\dx\d = \{[^\}]+\}\n', '', logic)

with open("logic.lua", "w") as f:
    f.write(logic)

