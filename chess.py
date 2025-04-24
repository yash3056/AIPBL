import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from game import Game

class Chess(Game):
    """A simplified implementation of Chess game."""
    
    # Piece values for evaluation
    PIECE_VALUES = {
        'p': 1,    # Pawn
        'n': 3,    # Knight
        'b': 3,    # Bishop
        'r': 5,    # Rook
        'q': 9,    # Queen
        'k': 100,  # King
    }
    
    def __init__(self):
        """Initialize the Chess game with the standard 8x8 board."""
        # We'll use a simplified representation where:
        # - Uppercase letters are white pieces: P, N, B, R, Q, K
        # - Lowercase letters are black pieces: p, n, b, r, q, k
        # - Empty squares are represented by '.'
        
        # The initial board
        self.initial_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        # Keep track of castling rights and other state
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rooks_moved = [False, False]  # [queenside, kingside]
        self.black_rooks_moved = [False, False]  # [queenside, kingside]
    
    def get_initial_state(self) -> Dict:
        """Return the initial state of the game."""
        return {
            'board': [row[:] for row in self.initial_board],
            'turn': 1,  # 1 for white, -1 for black
            'castling': {
                'white_king_moved': False,
                'black_king_moved': False,
                'white_rooks_moved': [False, False],
                'black_rooks_moved': [False, False]
            },
            'en_passant': None  # Store coordinates of pawn that moved two squares
        }
    
    def get_legal_moves(self, state: Dict) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Return a list of legal moves as ((from_row, from_col), (to_row, to_col)).
        
        In a real chess implementation, this would be much more complex.
        For this simplified version, we'll implement basic movement rules.
        """
        board = state['board']
        player = state['turn']
        moves = []
        
        # Determine which pieces belong to the current player
        pieces = 'PNBRQK' if player == 1 else 'pnbrqk'
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece in pieces:
                    # Get moves for this piece
                    piece_moves = self._get_piece_moves(state, row, col)
                    moves.extend(piece_moves)
        
        return moves
    
    def _get_piece_moves(self, state: Dict, row: int, col: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves for a piece at (row, col)."""
        board = state['board']
        piece = board[row][col]
        player = state['turn']
        moves = []
        
        piece_lower = piece.lower()
        
        # Pawn moves
        if piece_lower == 'p':
            moves.extend(self._get_pawn_moves(state, row, col))
        
        # Knight moves
        elif piece_lower == 'n':
            moves.extend(self._get_knight_moves(state, row, col))
        
        # Bishop moves
        elif piece_lower == 'b':
            moves.extend(self._get_diagonal_moves(state, row, col))
        
        # Rook moves
        elif piece_lower == 'r':
            moves.extend(self._get_straight_moves(state, row, col))
        
        # Queen moves (combination of bishop and rook)
        elif piece_lower == 'q':
            moves.extend(self._get_diagonal_moves(state, row, col))
            moves.extend(self._get_straight_moves(state, row, col))
        
        # King moves
        elif piece_lower == 'k':
            moves.extend(self._get_king_moves(state, row, col))
        
        return moves
    
    def _get_pawn_moves(self, state: Dict, row: int, col: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves for a pawn."""
        board = state['board']
        piece = board[row][col]
        player = state['turn']
        moves = []
        
        # Direction pawns move (white moves up, black moves down)
        direction = -1 if player == 1 else 1
        
        # Forward one square
        new_row = row + direction
        if 0 <= new_row < 8 and board[new_row][col] == '.':
            moves.append(((row, col), (new_row, col)))
            
            # Forward two squares from starting position
            start_row = 6 if player == 1 else 1
            if row == start_row:
                new_row = row + 2 * direction
                if 0 <= new_row < 8 and board[new_row][col] == '.':
                    moves.append(((row, col), (new_row, col)))
        
        # Captures (diagonally)
        for dc in [-1, 1]:
            new_col = col + dc
            new_row = row + direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target != '.':
                    # Check if it's an opponent's piece
                    if (player == 1 and target.islower()) or (player == -1 and target.isupper()):
                        moves.append(((row, col), (new_row, new_col)))
        
        return moves
    
    def _get_knight_moves(self, state: Dict, row: int, col: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves for a knight."""
        board = state['board']
        piece = board[row][col]
        player = state['turn']
        moves = []
        
        # Knight moves in L-shape
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                # Empty square or opponent's piece
                if target == '.' or (player == 1 and target.islower()) or (player == -1 and target.isupper()):
                    moves.append(((row, col), (new_row, new_col)))
        
        return moves
    
    def _get_diagonal_moves(self, state: Dict, row: int, col: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal diagonal moves (for bishop, queen)."""
        board = state['board']
        piece = board[row][col]
        player = state['turn']
        moves = []
        
        # Directions: up-left, up-right, down-left, down-right
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break  # Out of bounds
                
                target = board[new_row][new_col]
                if target == '.':
                    moves.append(((row, col), (new_row, new_col)))
                elif (player == 1 and target.islower()) or (player == -1 and target.isupper()):
                    # Can capture opponent's piece
                    moves.append(((row, col), (new_row, new_col)))
                    break  # Can't move further
                else:
                    break  # Blocked by own piece
        
        return moves
    
    def _get_straight_moves(self, state: Dict, row: int, col: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal straight moves (for rook, queen)."""
        board = state['board']
        piece = board[row][col]
        player = state['turn']
        moves = []
        
        # Directions: up, right, down, left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i * dr, col + i * dc
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break  # Out of bounds
                
                target = board[new_row][new_col]
                if target == '.':
                    moves.append(((row, col), (new_row, new_col)))
                elif (player == 1 and target.islower()) or (player == -1 and target.isupper()):
                    # Can capture opponent's piece
                    moves.append(((row, col), (new_row, new_col)))
                    break  # Can't move further
                else:
                    break  # Blocked by own piece
        
        return moves
    
    def _get_king_moves(self, state: Dict, row: int, col: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves for a king."""
        board = state['board']
        piece = board[row][col]
        player = state['turn']
        moves = []
        
        # All 8 directions
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target == '.' or (player == 1 and target.islower()) or (player == -1 and target.isupper()):
                    moves.append(((row, col), (new_row, new_col)))
        
        # Castling (simplified)
        castling = state['castling']
        if player == 1 and not castling['white_king_moved']:
            # Kingside castling for white
            if not castling['white_rooks_moved'][1] and all(board[7][i] == '.' for i in range(5, 7)):
                moves.append(((row, col), (7, 6)))  # King's move for castling
            
            # Queenside castling for white
            if not castling['white_rooks_moved'][0] and all(board[7][i] == '.' for i in range(1, 4)):
                moves.append(((row, col), (7, 2)))  # King's move for castling
                
        elif player == -1 and not castling['black_king_moved']:
            # Kingside castling for black
            if not castling['black_rooks_moved'][1] and all(board[0][i] == '.' for i in range(5, 7)):
                moves.append(((row, col), (0, 6)))  # King's move for castling
            
            # Queenside castling for black
            if not castling['black_rooks_moved'][0] and all(board[0][i] == '.' for i in range(1, 4)):
                moves.append(((row, col), (0, 2)))  # King's move for castling
        
        return moves
    
    def get_next_state(self, state: Dict, move: Tuple[Tuple[int, int], Tuple[int, int]]) -> Dict:
        """Return the state after making the move."""
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Create a deep copy of the current state
        new_state = {
            'board': [row[:] for row in state['board']],
            'turn': -state['turn'],  # Switch players
            'castling': {
                'white_king_moved': state['castling']['white_king_moved'],
                'black_king_moved': state['castling']['black_king_moved'],
                'white_rooks_moved': state['castling']['white_rooks_moved'][:],
                'black_rooks_moved': state['castling']['black_rooks_moved'][:]
            },
            'en_passant': None
        }
        
        board = new_state['board']
        piece = board[from_row][from_col]
        
        # Update castling rights if king or rook moves
        if piece == 'K':
            new_state['castling']['white_king_moved'] = True
        elif piece == 'k':
            new_state['castling']['black_king_moved'] = True
        elif piece == 'R':
            if from_row == 7:
                if from_col == 0:  # Queenside rook
                    new_state['castling']['white_rooks_moved'][0] = True
                elif from_col == 7:  # Kingside rook
                    new_state['castling']['white_rooks_moved'][1] = True
        elif piece == 'r':
            if from_row == 0:
                if from_col == 0:  # Queenside rook
                    new_state['castling']['black_rooks_moved'][0] = True
                elif from_col == 7:  # Kingside rook
                    new_state['castling']['black_rooks_moved'][1] = True
        
        # Handle castling moves
        if piece.lower() == 'k' and abs(from_col - to_col) > 1:
            # This is a castling move
            if to_col == 6:  # Kingside castling
                # Move the rook as well
                rook_row = from_row
                board[rook_row][5] = board[rook_row][7]  # Move rook
                board[rook_row][7] = '.'  # Remove rook from original position
            elif to_col == 2:  # Queenside castling
                # Move the rook as well
                rook_row = from_row
                board[rook_row][3] = board[rook_row][0]  # Move rook
                board[rook_row][0] = '.'  # Remove rook from original position
        
        # Make the main move
        board[to_row][to_col] = board[from_row][from_col]
        board[from_row][from_col] = '.'
        
        return new_state
    
    def is_terminal_state(self, state: Dict) -> bool:
        """Check if the game is over."""
        return self.get_winner(state) is not None
    
    def get_winner(self, state: Dict) -> Optional[int]:
        """
        Return the winner of the game (1 for white, -1 for black, 0 for draw, None if game not over).
        In a real chess implementation, this would check for checkmate, stalemate, etc.
        For simplicity, we'll just check if a king is captured.
        """
        board = state['board']
        
        # Check if any king is missing (simplified check)
        white_king_exists = any(any(piece == 'K' for piece in row) for row in board)
        black_king_exists = any(any(piece == 'k' for piece in row) for row in board)
        
        if not white_king_exists:
            return -1  # Black wins
        if not black_king_exists:
            return 1   # White wins
            
        # Check for no legal moves (stalemate)
        if not self.get_legal_moves(state):
            return 0  # Draw
            
        # Game not over
        return None
    
    def evaluate(self, state: Dict, player: int) -> float:
        """
        Evaluate the board from player's perspective.
        This is a simple material-based evaluation.
        """
        board = state['board']
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    piece_value = self.PIECE_VALUES[piece.lower()]
                    # White pieces are uppercase, black pieces are lowercase
                    if piece.isupper():  # White piece
                        score += piece_value
                    else:  # Black piece
                        score -= piece_value
        
        # Adjust the score based on the player
        return score if player == 1 else -score
    
    def print_state(self, state: Dict) -> None:
        """Print a human-readable representation of the board."""
        board = state['board']
        player = "White" if state['turn'] == 1 else "Black"
        
        print(f"\nCurrent player: {player}")
        print("  a b c d e f g h")
        for i, row in enumerate(board):
            print(f"{8-i} {' '.join(row)} {8-i}")
        print("  a b c d e f g h")