local p1_path_5x5 = {{2,4},{3,4},{4,4},{4,3},{4,2},{4,1},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{1,4},{1,3},{2,3},{3,3},{3,2},{3,1},{2,1},{1,1},{1,2},{2,2}}
local p2_path_5x5 = {{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{1,4},{2,4},{3,4},{4,4},{4,3},{4,2},{4,1},{4,0},{3,0},{3,1},{2,1},{1,1},{1,2},{1,3},{2,3},{3,3},{3,2},{2,2}}
local p3_path_5x5 = {{0,2},{0,3},{0,4},{1,4},{2,4},{3,4},{4,4},{4,3},{4,2},{4,1},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{1,1},{1,2},{1,3},{2,3},{3,3},{3,2},{3,1},{2,1},{2,2}}
local p4_path_5x5 = {{4,2},{4,1},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{1,4},{2,4},{3,4},{4,4},{4,3},{3,3},{3,2},{3,1},{2,1},{1,1},{1,2},{1,3},{2,3},{2,2}}

local p1_path_7x7 = {{3,6},{4,6},{5,6},{6,6},{6,5},{6,4},{6,3},{6,2},{6,1},{6,0},{5,0},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{0,5},{0,6},{1,6},{2,6},{2,5},{3,5},{4,5},{5,5},{5,4},{5,3},{5,2},{5,1},{4,1},{3,1},{2,1},{1,1},{1,2},{1,3},{1,4},{1,5},{2,4},{3,4},{4,4},{4,3},{4,2},{3,2},{2,2},{2,3},{3,3}}
local p2_path_7x7 = {{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{0,5},{0,6},{1,6},{2,6},{3,6},{4,6},{5,6},{6,6},{6,5},{6,4},{6,3},{6,2},{6,1},{6,0},{5,0},{4,0},{4,1},{3,1},{2,1},{1,1},{1,2},{1,3},{1,4},{1,5},{2,5},{3,5},{4,5},{5,5},{5,4},{5,3},{5,2},{5,1},{4,2},{3,2},{2,2},{2,3},{2,4},{3,4},{4,4},{4,3},{3,3}}
local p3_path_7x7 = {{0,3},{0,4},{0,5},{0,6},{1,6},{2,6},{3,6},{4,6},{5,6},{6,6},{6,5},{6,4},{6,3},{6,2},{6,1},{6,0},{5,0},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{1,2},{1,3},{1,4},{1,5},{2,5},{3,5},{4,5},{5,5},{5,4},{5,3},{5,2},{5,1},{4,1},{3,1},{2,1},{1,1},{2,2},{2,3},{2,4},{3,4},{4,4},{4,3},{4,2},{3,2},{3,3}}
local p4_path_7x7 = {{6,3},{6,2},{6,1},{6,0},{5,0},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{0,5},{0,6},{1,6},{2,6},{3,6},{4,6},{5,6},{6,6},{6,5},{6,4},{5,4},{5,3},{5,2},{5,1},{4,1},{3,1},{2,1},{1,1},{1,2},{1,3},{1,4},{1,5},{2,5},{3,5},{4,5},{5,5},{4,4},{4,3},{4,2},{3,2},{2,2},{2,3},{2,4},{3,4},{3,3}}

local function get_variant()
    local v = game.get_variation and game.get_variation() or "5x5"
    if v == "7x7" then return "7x7" end
    return "5x5"
end

local function get_max_pos()
    if get_variant() == "7x7" then return 49 else return 25 end
end

local function get_physical(player, pos, variant)
    if pos == 0 then return {-1, -1} end
    if variant == "7x7" then
        if player == 0 then return p1_path_7x7[pos] end
        if player == 1 then return p2_path_7x7[pos] end
        if player == 2 then return p3_path_7x7[pos] end
        if player == 3 then return p4_path_7x7[pos] end
    else
        if player == 0 then return p1_path_5x5[pos] end
        if player == 1 then return p2_path_5x5[pos] end
        if player == 2 then return p3_path_5x5[pos] end
        if player == 3 then return p4_path_5x5[pos] end
    end
    return {-1, -1}
end

local function get_path_index(player, x, y, variant)
    local path
    if variant == "7x7" then
        if player == 0 then path = p1_path_7x7
        elseif player == 1 then path = p2_path_7x7
        elseif player == 2 then path = p3_path_7x7
        elseif player == 3 then path = p4_path_7x7
        else return -1 end
    else
        if player == 0 then path = p1_path_5x5
        elseif player == 1 then path = p2_path_5x5
        elseif player == 2 then path = p3_path_5x5
        elseif player == 3 then path = p4_path_5x5
        else return -1 end
    end
    
    for i, coords in ipairs(path) do
        if coords[1] == x and coords[2] == y then
            return i
        end
    end
    return -1
end

local function is_safe(x, y, variant)
    local safe
    if variant == "7x7" then
        safe = {{0,0}, {0,3}, {0,6}, {1,1}, {1,5}, {3,0}, {3,3}, {3,6}, {5,1}, {5,5}, {6,0}, {6,3}, {6,6}}
    else
        safe = {{2,4}, {4,2}, {2,0}, {0,2}, {2,2}}
    end
    for _, s in ipairs(safe) do
        if s[1] == x and s[2] == y then return true end
    end
    return false
end

function setup(players)
    local var = get_variant()
    game.set_var("variation", var)
    local pieces = {}
    for i, p in ipairs(players) do
        local p_str = "P" .. tostring(i)
        
        local start_pos = get_physical(i-1, 1, var)
        local pos_str = start_pos[1] .. "," .. start_pos[2]
        
        if var == "7x7" then
            pieces[p_str] = {1, 1, 1, 1, 1, 1}
            for j=1, 6 do
                game.place_piece("pawn", pos_str, i-1)
            end
        else
            pieces[p_str] = {1, 1, 1, 1}
            for j=1, 4 do
                game.place_piece("pawn", pos_str, i-1)
            end
        end
    end
    game.set_var("pieces", pieces)
    game.set_var("phase", "roll")
    game.set_var("lastRoll", 1)
    game.set_var("message", "Game start! (" .. var .. ") Player 1 to roll.")
end

function get_actions()
    local current = game.current_player()
    local phase = game.get_var("phase") or "roll"
    local pieces = game.get_var("pieces") or {}
    local max_pos = get_max_pos()
    
    local actions = {}
    if phase == "roll" then
        table.insert(actions, {id = "roll", name = "Roll Dice", type = "button"})
    elseif phase == "move" then
        local p_str = "P" .. tostring(current + 1)
        local has_valid_moves = false
        if pieces[p_str] then
            for i, pos in ipairs(pieces[p_str]) do
                if pos + game.get_var("lastRoll") <= max_pos then
                    has_valid_moves = true
                    break
                end
            end
        end
        if has_valid_moves then
            table.insert(actions, {id = "move_piece", name = "Move Piece", type = "selectPiece"})
        else
            table.insert(actions, {id = "end_turn", name = "End Turn", type = "button"})
        end
    end
    
    if #actions == 0 then
        table.insert(actions, {id = "end_turn", name = "End Turn", type = "button"})
    end
    return actions
end

local function handle_capture(player, new_pos_str, pieces, variant)
    local x, y = string.match(new_pos_str, "(%d+),(%d+)")
    x, y = tonumber(x), tonumber(y)
    
    if is_safe(x, y, variant) then return false, pieces end
    
    local captured = false
    local max_iters = 10
    local iters = 0
    while iters < max_iters do
        iters = iters + 1
        local p = board.get_piece(new_pos_str)
        if not p or p.owner_index == player then 
            break 
        end
        
        local opp = p.owner_index
        local start_pos = get_physical(opp, 1, variant)
        local opp_str = "P" .. tostring(opp + 1)
        
        -- Update state array
        local old_idx = get_path_index(opp, x, y, variant)
        if old_idx ~= -1 and pieces[opp_str] then
            for i, pos in ipairs(pieces[opp_str]) do
                if pos == old_idx then
                    pieces[opp_str][i] = 1
                    break
                end
            end
        end
        
        game.move_piece(p.id, start_pos[1] .. "," .. start_pos[2])
        captured = true
    end
    
    return captured, pieces
end

function on_move(player_index, action_id, move)
    if player_index ~= game.current_player() then return false, "Not your turn" end

    local phase = game.get_var("phase")
    local pieces = game.get_var("pieces")
    local p_str = "P" .. tostring(player_index + 1)
    local var = get_variant()
    local max_pos = get_max_pos()
    
    if action_id == "roll" and phase == "roll" then
        local roll
        if var == "7x7" then
            local val = math.random(1, 7)
            roll = (val == 7) and 12 or val
        else
            local val = math.random(1, 5)
            roll = (val == 5) and 8 or val
        end
        game.set_var("lastRoll", roll)
        
        local can_move = false
        if pieces[p_str] then
            for i, pos in ipairs(pieces[p_str]) do
                if pos + roll <= max_pos then
                    can_move = true
                    break
                end
            end
        end
        
        if can_move then
            game.set_var("phase", "move")
            game.set_var("message", "Player " .. (player_index+1) .. " rolled " .. roll)
        else
            game.set_var("message", "Player " .. (player_index+1) .. " rolled " .. roll .. " but has no valid moves.")
            game.set_var("phase", "roll")
            game.end_turn()
        end
        return true
        
    elseif action_id == "move_piece" and phase == "move" then
        local roll = game.get_var("lastRoll")
        local piece_id = move.piece_id
        if not piece_id then return false, "No piece selected" end
        
        local pos_str = piece.position(piece_id)
        if not pos_str then return false, "Piece not found" end
        
        local x, y = string.match(pos_str, "(%d+),(%d+)")
        x, y = tonumber(x), tonumber(y)
        
        local path_idx = get_path_index(player_index, x, y, var)
        if path_idx == -1 then return false, "Piece not on path" end
        
        if path_idx + roll <= max_pos then
            -- Update state array
            for i, pos in ipairs(pieces[p_str]) do
                if pos == path_idx then
                    pieces[p_str][i] = path_idx + roll
                    break
                end
            end
            
            local new_idx = path_idx + roll
            local new_coords = get_physical(player_index, new_idx, var)
            local new_pos_str = new_coords[1] .. "," .. new_coords[2]
            
            -- Handle captures BEFORE moving my piece
            local captured
            captured, pieces = handle_capture(player_index, new_pos_str, pieces, var)
            game.set_var("pieces", pieces)
            
            game.move_piece(piece_id, new_pos_str)
            
            local gets_extra = (roll == 4 or roll == 8 or roll == 12 or captured)
            game.set_var("phase", "roll")
            
            if gets_extra then
                game.set_var("message", "Player " .. (player_index+1) .. " gets an extra turn!")
            else
                game.end_turn()
            end
            return true
        end
    elseif action_id == "end_turn" then
        game.set_var("phase", "roll")
        game.end_turn()
        return true
    end
    
    return false, "Invalid move"
end

function check_win()
    local pieces = game.get_var("pieces")
    local max_pos = get_max_pos()
    if not pieces then return nil end
    for p_str, p_pieces in pairs(pieces) do
        local won = true
        for _, pos in ipairs(p_pieces) do
            if pos < max_pos then won = false break end
        end
        if won then 
            local w_idx = tonumber(string.sub(p_str, 2)) - 1
            return {winner = w_idx} 
        end
    end
    return nil
end
