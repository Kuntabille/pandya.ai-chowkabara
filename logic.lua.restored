import json

logic_lua = """local p1_path_5x5 = {{2,4},{3,4},{4,4},{4,3},{4,2},{4,1},{4,0},{3,0},{2,0},{1,0},{0,0},{0,1},{0,2},{0,3},{0,4},{1,4},{1,3},{2,3},{3,3},{3,2},{3,1},{2,1},{1,1},{1,2},{2,2}}
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
        safe = {{3,6}, {6,3}, {3,0}, {0,3}, {3,5}, {5,3}, {3,1}, {1,3}, {3,3}}
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
        pieces[p_str] = {1, 1, 1, 1}
        
        local start_pos = get_physical(i-1, 1, var)
        local pos_str = start_pos[1] .. "," .. start_pos[2]
        
        game.place_piece("pawn", pos_str, i-1)
        game.place_piece("pawn", pos_str, i-1)
        game.place_piece("pawn", pos_str, i-1)
        game.place_piece("pawn", pos_str, i-1)
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
        local val = math.random(1, 5)
        local roll = (val == 5) and 8 or val
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
            
            local gets_extra = (roll == 4 or roll == 8 or captured)
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
"""

with open("logic.lua", "w") as f:
    f.write(logic_lua)

component_tsx = """import React from 'react';

export default function CustomGameBoard({ gameState, onMove, currentPlayerId }: { gameState: any, onMove: any, currentPlayerId: string }) {
  if (!gameState || !gameState.variables) {
    return <div>Loading Game State...</div>;
  }

  const variant = gameState.variables?.variation || "5x5";
  const gridLength = variant === "7x7" ? 7 : 5;
  const CELL_SIZE = variant === "7x7" ? 60 : 80;
  const BOARD_SIZE = gridLength * CELL_SIZE;
  
  const safeSquares = variant === "7x7" 
    ? [[3,6], [6,3], [3,0], [0,3], [3,5], [5,3], [3,1], [1,3], [3,3]]
    : [[2,4], [4,2], [2,0], [0,2], [2,2]];

  const isSafe = (x: number, y: number) => {
    return safeSquares.some(s => s[0] === x && s[1] === y);
  };

  let boardRotation = 0;
  if (currentPlayerId === '1') boardRotation = 180;
  else if (currentPlayerId === '2') boardRotation = 270;
  else if (currentPlayerId === '3') boardRotation = 90;

  const colorMap: any = { 0: '#e74c3c', 1: '#3498db', 2: '#f1c40f', 3: '#2ecc71' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', fontFamily: 'sans-serif', background: '#2c3e50', color: 'white', minHeight: '100vh', padding: 20 }}>
      <div style={{ marginBottom: 20, fontSize: 18, fontWeight: 'bold' }}>
        {gameState.variables?.message}
      </div>

      <div style={{ display: 'flex', gap: 20, marginBottom: 20, alignItems: 'center', height: 80 }}>
        {gameState.variables?.phase === 'roll' ? (
          // @ts-ignore
          <Dice 
            id="main_dice" 
            results={[gameState.variables?.lastRoll || 1]} 
            sides={8} 
            onMove={onMove} 
          />
        ) : (
          <div style={{ padding: '10px 20px', fontSize: 16, background: '#34495e', color: 'white', borderRadius: 4, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            Last Roll: {gameState.variables?.lastRoll}
          </div>
        )}
      </div>

      <div style={{ position: 'relative', width: BOARD_SIZE + 100, height: BOARD_SIZE + 100 }}>
        {/* The SVG Board */}
        <svg width={BOARD_SIZE + 100} height={BOARD_SIZE + 100} style={{ position: 'absolute', top: 0, left: 0, background: '#ecf0f1', borderRadius: 8, boxShadow: '0 4px 6px rgba(0,0,0,0.3)', transform: `rotate(${boardRotation}deg)`, transition: 'transform 0.5s ease-in-out' }}>
          <g transform="translate(50, 50)">
            {Array.from({ length: gridLength }).map((_, y) => 
              Array.from({ length: gridLength }).map((_, x) => {
                const isSafeSquare = isSafe(x, y);
                return (
                  <rect
                    key={`${x}-${y}`}
                    x={x * CELL_SIZE}
                    y={y * CELL_SIZE}
                    width={CELL_SIZE}
                    height={CELL_SIZE}
                    fill={isSafeSquare ? '#bdc3c7' : '#ffffff'}
                    stroke="#34495e"
                    strokeWidth={2}
                  />
                );
              })
            )}
            {safeSquares.map(([x, y]) => (
               <g key={`cross-${x}-${y}`}>
                 <line x1={x * CELL_SIZE} y1={y * CELL_SIZE} x2={(x + 1) * CELL_SIZE} y2={(y + 1) * CELL_SIZE} stroke="#34495e" strokeWidth={2} />
                 <line x1={(x + 1) * CELL_SIZE} y1={y * CELL_SIZE} x2={x * CELL_SIZE} y2={(y + 1) * CELL_SIZE} stroke="#34495e" strokeWidth={2} />
               </g>
            ))}
          </g>
        </svg>

        {/* The Pieces Overlay */}
        <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', transform: `rotate(${boardRotation}deg)`, transition: 'transform 0.5s ease-in-out' }}>
          {gameState.pieces?.map((piece: any) => {
            const coords = piece.position.split(',');
            if (coords.length !== 2) return null;
            
            const x = parseInt(coords[0]);
            const y = parseInt(coords[1]);
            let cx = 50 + x * CELL_SIZE + CELL_SIZE / 2;
            let cy = 50 + y * CELL_SIZE + CELL_SIZE / 2;
            
            // Cluster pieces on the same square
            const piecesOnSquare = gameState.pieces.filter((p: any) => p.position === piece.position);
            const pieceIndex = piecesOnSquare.findIndex((p: any) => p.id === piece.id);
            const offsetX = piecesOnSquare.length > 1 ? ((pieceIndex % 2 === 0) ? -15 : 15) : 0;
            const offsetY = piecesOnSquare.length > 1 ? ((pieceIndex < 2) ? -15 : 15) : 0;

            const isMyTurn = gameState.currentPlayerIndex === piece.ownerIndex;
            const isMe = String(piece.ownerIndex) === currentPlayerId;
            const canMove = isMyTurn && isMe && gameState.variables?.phase === 'move';

            return (
              <div 
                key={piece.id}
                style={{
                  position: 'absolute',
                  left: cx + offsetX - 20,
                  top: cy + offsetY - 20,
                  width: 40,
                  height: 40,
                  pointerEvents: 'auto',
                  cursor: canMove ? 'pointer' : 'default',
                  transform: `rotate(${-boardRotation}deg)`,
                  transition: 'all 0.3s ease-in-out',
                  zIndex: 10 + pieceIndex
                }}
              >
                {/* @ts-ignore */}
                <Pawn
                  id={piece.id}
                  color={colorMap[piece.ownerIndex]}
                  ownerIndex={piece.ownerIndex}
                  onClick={() => {
                    if (canMove) {
                      onMove({ actionId: 'move_piece', piece_id: piece.id });
                    }
                  }}
                />
              </div>
            );
          })}
        </div>
      </div>
      
      <div style={{ marginTop: 20, display: 'flex', gap: 20 }}>
        <p><strong style={{ color: '#e74c3c' }}>Player 1 (Red):</strong> Bottom</p>
        <p><strong style={{ color: '#3498db' }}>Player 2 (Blue):</strong> Top</p>
        <p><strong style={{ color: '#f1c40f' }}>Player 3 (Yellow):</strong> Left</p>
        <p><strong style={{ color: '#2ecc71' }}>Player 4 (Green):</strong> Right</p>
      </div>
    </div>
  );
}
"""

with open("component.tsx", "w") as f:
    f.write(component_tsx)

