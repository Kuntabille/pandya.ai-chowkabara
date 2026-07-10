import re

with open("logic.lua", "r") as f:
    logic = f.read()

new_get_physical = """local function get_physical(player, pos, variant)
    if pos == 0 then return {-1, -1} end
    
    local path_id = "p" .. (player + 1) .. "_path"
    local nodes = paths.get_nodes(path_id)
    if not nodes or #nodes == 0 then
        -- SIMULATION WORKAROUND
        local fallback = get_fallback_path(player, variant)
        if fallback and #fallback >= pos then
            return {fallback[pos][1], fallback[pos][2]}
        end
        return {-1, -1}
    end
    
    if nodes and #nodes >= pos then
        local coord_str = nodes[pos]
        local x, y = coord_str:match("(%d+),(%d+)")
        if x and y then
            return {tonumber(x), tonumber(y)}
        end
    end
    return {-1, -1}
end"""

logic = re.sub(r'local function get_physical\(player, pos, variant\).*?return \{-1, -1\}\nend', new_get_physical, logic, flags=re.DOTALL)

new_get_path_index = """local function get_path_index(player, x, y, variant)
    local path_id = "p" .. (player + 1) .. "_path"
    local nodes = paths.get_nodes(path_id)
    if not nodes or #nodes == 0 then
        -- SIMULATION WORKAROUND
        local fallback = get_fallback_path(player, variant)
        if fallback then
            for i, node in ipairs(fallback) do
                if node[1] == x and node[2] == y then
                    return i
                end
            end
        end
        return -1
    end

    if nodes then
        local target_str = x .. "," .. y
        for i, node in ipairs(nodes) do
            if node == target_str then
                return i
            end
        end
    end
    return -1
end"""

logic = re.sub(r'local function get_path_index\(player, x, y, variant\).*?return -1\nend', new_get_path_index, logic, flags=re.DOTALL)

with open("logic.lua", "w") as f:
    f.write(logic)
