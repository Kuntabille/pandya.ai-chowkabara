with open("logic.lua", "r") as f:
    logic = f.read()

path_index_func = """
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
end
"""

if "local function get_path_index" not in logic:
    logic = logic.replace("local function is_safe", path_index_func + "\n\nlocal function is_safe")
    with open("logic.lua", "w") as f:
        f.write(logic)
        print("Added get_path_index")
