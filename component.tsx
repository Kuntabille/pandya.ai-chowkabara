import React from 'react';

export default function CustomGameBoard({ gameState, onMove, currentPlayerId }: { gameState: any, onMove: any, currentPlayerId: string }) {
  if (!gameState || !gameState.variables) {
    return <div>Loading Game State...</div>;
  }

  const variant = gameState.variables?.variation || "5x5";
  const gridLength = variant === "7x7" ? 7 : 5;
  const CELL_SIZE = variant === "7x7" ? 60 : 80;
  const BOARD_SIZE = gridLength * CELL_SIZE;
  
  const safeSquares = variant === "7x7" 
    ? [[0,0], [0,3], [0,6], [1,1], [1,5], [3,0], [3,3], [3,6], [5,1], [5,5], [6,0], [6,3], [6,6]]
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
