with open("logic.lua", "r") as f:
    logic = f.read()

fallback_paths = """
local p1_path_5x5 = {{2,4},{3,4},{4,4},{4,3},{4,2},{4,1},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{1,4},{1,3},{2,3},{3,3},{3,2},{3,1},{2,1},{1,1},{1,2},{2,2}}
local p2_path_5x5 = {{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{1,4},{2,4},{3,4},{4,4},{4,3},{4,2},{4,1},{4,0},{3,0},{3,1},{2,1},{1,1},{1,2},{1,3},{2,3},{3,3},{3,2},{2,2}}
local p3_path_5x5 = {{0,2},{0,3},{0,4},{1,4},{2,4},{3,4},{4,4},{4,3},{4,2},{4,1},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{1,1},{1,2},{1,3},{2,3},{3,3},{3,2},{3,1},{2,1},{2,2}}
local p4_path_5x5 = {{4,2},{4,1},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{1,4},{2,4},{3,4},{4,4},{4,3},{3,3},{3,2},{3,1},{2,1},{1,1},{1,2},{1,3},{2,3},{2,2}}

local p1_path_7x7 = {{3,6},{4,6},{5,6},{6,6},{6,5},{6,4},{6,3},{6,2},{6,1},{6,0},{5,0},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{0,5},{0,6},{1,6},{2,6},{2,5},{3,5},{4,5},{5,5},{5,4},{5,3},{5,2},{5,1},{4,1},{3,1},{2,1},{1,1},{1,2},{1,3},{1,4},{1,5},{2,4},{3,4},{4,4},{4,3},{4,2},{3,2},{2,2},{2,3},{3,3}}
local p2_path_7x7 = {{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{0,5},{0,6},{1,6},{2,6},{3,6},{4,6},{5,6},{6,6},{6,5},{6,4},{6,3},{6,2},{6,1},{6,0},{5,0},{4,0},{4,1},{3,1},{2,1},{1,1},{1,2},{1,3},{1,4},{1,5},{2,5},{3,5},{4,5},{5,5},{5,4},{5,3},{5,2},{5,1},{4,2},{3,2},{2,2},{2,3},{2,4},{3,4},{4,4},{4,3},{3,3}}
local p3_path_7x7 = {{0,3},{0,4},{0,5},{0,6},{1,6},{2,6},{3,6},{4,6},{5,6},{6,6},{6,5},{6,4},{6,3},{6,2},{6,1},{6,0},{5,0},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{1,2},{1,3},{1,4},{1,5},{2,5},{3,5},{4,5},{5,5},{5,4},{5,3},{5,2},{5,1},{4,1},{3,1},{2,1},{1,1},{2,2},{2,3},{2,4},{3,4},{4,4},{4,3},{4,2},{3,2},{3,3}}
local p4_path_7x7 = {{6,3},{6,2},{6,1},{6,0},{5,0},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{0,5},{0,6},{1,6},{2,6},{3,6},{4,6},{5,6},{6,6},{6,5},{6,4},{5,4},{5,3},{5,2},{5,1},{4,1},{3,1},{2,1},{1,1},{1,2},{1,3},{1,4},{1,5},{2,5},{3,5},{4,5},{5,5},{4,4},{4,3},{4,2},{3,2},{2,2},{2,3},{2,4},{3,4},{3,3}}

local function get_fallback_path(player, variant)
    if variant == "7x7" then
        if player == 0 then return p1_path_7x7 end
        if player == 1 then return p2_path_7x7 end
        if player == 2 then return p3_path_7x7 end
        if player == 3 then return p4_path_7x7 end
    else
        if player == 0 then return p1_path_5x5 end
        if player == 1 then return p2_path_5x5 end
        if player == 2 then return p3_path_5x5 end
        if player == 3 then return p4_path_5x5 end
    end
    return {}
end
"""

logic = fallback_paths + "\n" + logic

import re

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
        return {nodes[pos].x, nodes[pos].y}
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
        for i, node in ipairs(nodes) do
            if node.x == x and node.y == y then
                return i
            end
        end
    end
    return -1
end"""

logic = re.sub(r'local function get_path_index\(player, x, y, variant\).*?return -1\nend', new_get_path_index, logic, flags=re.DOTALL)

with open("logic.lua", "w") as f:
    f.write(logic)

