import re

with open("logic.lua", "r") as f:
    logic = f.read()

# Add get_mapped_path_index
logic = logic.replace("local function get_fallback_path", """local function get_mapped_path_index(player_index, num_players)
    if num_players == 2 then
        if player_index == 0 then return 0 end
        if player_index == 1 then return 2 end
    elseif num_players == 3 then
        if player_index == 0 then return 0 end
        if player_index == 1 then return 1 end
        if player_index == 2 then return 2 end
    end
    return player_index
end

local function get_fallback_path""")

# Update get_physical
old_get_physical = """local function get_physical(player, pos, variant)
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

logic = logic.replace(old_get_physical, new_get_physical)

# Update get_path_index
old_get_path_index = """local function get_path_index(player, x, y, variant)
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

logic = logic.replace(old_get_path_index, new_get_path_index)

# Update setup to store num_players
logic = logic.replace('game.set_var("variation", var)', 'game.set_var("variation", var)\n    game.set_var("num_players", #players)')

with open("logic.lua", "w") as f:
    f.write(logic)
