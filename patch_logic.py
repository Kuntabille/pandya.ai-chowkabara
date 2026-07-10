import re

with open("logic.lua", "r") as f:
    content = f.read()

# Remove the fallback arrays
content = re.sub(r'local p1_path_5x5.*?p4_path_7x7 = \{\{.*?\}\}\n', '', content, flags=re.DOTALL)

# Remove get_fallback_path
content = re.sub(r'local function get_fallback_path.*?end\n', '', content, flags=re.DOTALL)

# Update get_physical to remove simulation workaround
old_get_physical = """local function get_physical(player, pos, variant)
    if pos == 0 then return {-1, -1} end
    
    local num_players = game.get_var("num_players") or 4
    local mapped = get_mapped_path_index(player, num_players)
    
    local path_id = "p" .. (mapped + 1) .. "_path"
    local nodes = paths.get_nodes(path_id)
    if not nodes or #nodes == 0 then
        -- SIMULATION WORKAROUND
        local fallback = get_fallback_path(mapped, variant)
        if fallback and #fallback >= pos then
            return {fallback[pos][1], fallback[pos][2]}
        end
        return {-1, -1}
    end
    
    if nodes and #nodes >= pos then
        return {nodes[pos].x, nodes[pos].y}
    end
    return {-1, -1}
end"""

new_get_physical = """local function get_physical(player, pos, variant)
    if pos == 0 then return {-1, -1} end
    
    local num_players = game.get_var("num_players") or 4
    local mapped = get_mapped_path_index(player, num_players)
    
    local path_id = "p" .. (mapped + 1) .. "_path"
    local nodes = paths.get_nodes(path_id)
    
    if nodes and #nodes >= pos then
        return {nodes[pos].x, nodes[pos].y}
    end
    return {-1, -1}
end"""

content = content.replace(old_get_physical, new_get_physical)


# Update get_path_index
old_get_path_index = """local function get_path_index(player, x, y, variant)
    local num_players = game.get_var("num_players") or 4
    local mapped = get_mapped_path_index(player, num_players)

    local path_id = "p" .. (mapped + 1) .. "_path"
    local nodes = paths.get_nodes(path_id)
    if not nodes or #nodes == 0 then
        -- SIMULATION WORKAROUND
        local fallback = get_fallback_path(mapped, variant)
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
        for i, node in ipairs(nodes) do
            if node.x == x and node.y == y then
                return i
            end
        end
    end
    return -1
end"""

new_get_path_index = """local function get_path_index(player, x, y, variant)
    local num_players = game.get_var("num_players") or 4
    local mapped = get_mapped_path_index(player, num_players)

    local path_id = "p" .. (mapped + 1) .. "_path"
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

content = content.replace(old_get_path_index, new_get_path_index)

with open("logic.lua", "w") as f:
    f.write(content)

