# Chowka Bara

## 1. Overview & Objective
Chowka Bara is a traditional Indian racing board game, similar to Ludo. Players race their pawns from their starting positions to the center of the board. The first player to successfully move all of their pawns into the central winning square is declared the winner! 

## 2. Components & Board Setup
The game can be played in two variations: **5x5** and **7x7**.
- **The Board:** A grid of either 5x5 or 7x7 squares. The board contains specific "safe squares" marked with an X. Pawns on safe squares cannot be captured.
- **Pawns:** Each player controls a set of pawns (4 pawns for the 5x5 variant, and 6 pawns for the 7x7 variant). Players start with all pawns on their respective starting safe squares at the edges of the board.
- **Cowrie Shells:** Instead of standard dice, the game uses Cowrie shells (4 shells for the 5x5 variant, and 6 shells for the 7x7 variant). Each shell can land face-up or face-down.

## 3. Turn Structure & Available Actions
A player's turn consists of two phases: **Roll** and **Move**.
- **Roll Phase (`roll`):** Click the cowrie shells in the UI to roll them and determine your movement value.
- **Move Phase (`move_piece`):** Click one of your pawns to advance it along the path by the number of squares rolled.
- **End Turn (`end_turn`):** If a player rolls but has no valid moves, their turn ends automatically.

## 4. Complete Rules & Mechanics Breakdown

### Rolling the Cowries
The number of squares you can move depends on how many shells land face-up (showing the opening):
- **5x5 Variant (4 shells):** 
  - 1 face-up = 1 square
  - 2 face-up = 2 squares
  - 3 face-up = 3 squares
  - 4 face-up = 4 squares (Grants an extra turn!)
  - 0 face-up = 8 squares (Grants an extra turn!)
- **7x7 Variant (6 shells):**
  - 1-5 face-up = 1-5 squares respectively
  - 6 face-up = 6 squares
  - 0 face-up = 12 squares (Grants an extra turn!)
  - Rolling a 4, 8, or 12 grants an extra turn in either variant.

### Movement & Pathing
- Pawns follow a spiral path along the board, completing the outer ring before stepping into the inner ring, eventually spiraling inward to the exact center square.
- A pawn must reach the center square by an exact roll. If the roll is higher than the remaining distance, that pawn cannot move.

### Capturing & Safe Squares
- If you land exactly on an opponent's pawn, you **capture** it! The captured pawn is sent all the way back to its starting square, and you are granted an **extra turn**.
- **Safe Squares:** Squares marked with an "X" are safe. Multiple pawns (even from different players) can coexist on a safe square without capturing each other.
- Note: Many regional rules require a player to capture at least one opponent's pawn before being allowed to enter the inner rings, but this implementation allows inward movement automatically.

## 5. Sample Gameplay
1. **Player 1 (Red)** begins. They click the cowrie shells to roll. 3 shells land face up.
2. Player 1 selects one of their pawns to move it 3 spaces forward along their path. 
3. Because they did not roll an extra-turn value (4, 8, 12) or capture an opponent, their turn ends.
4. **Player 2 (Blue)** rolls 0 face-up shells on the 5x5 board, scoring an 8! They move a pawn 8 spaces and get to roll again.
5. On their bonus roll, Player 2 rolls a 2. They advance a pawn 2 spaces, landing exactly on an unsafe square occupied by Player 1. Player 1's pawn is captured and sent back to start, giving Player 2 yet another bonus roll!

## 6. Beginner Strategy & Tips
- **Stack on Safe Squares:** Try to land your pawns on the marked safe squares whenever possible to protect them from capture.
- **Spread Out Your Pawns:** Don't just race one pawn to the center. Having multiple pawns spread across the board increases your chances of capturing opponents and gives you flexibility if you roll a number that one pawn can't use.
- **Control the Choke Points:** The entrance to the inner rings can become a bloodbath. Use safe squares near these transitions to ambush opponents as they try to pass.
