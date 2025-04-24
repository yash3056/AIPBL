import numpy as np
from typing import List, Tuple, Optional, Any
from game import Game

class TicTacToe(Game):
    """Implementation of Tic-Tac-Toe game."""
    
    def __init__(self, board_size: int = 3):
        """
        Initialize the Tic-Tac-Toe game.
        
        Args:
            board_size: Size of the board (board_size x board_size)
        """
        self.board_size = board_size
    
    def get_initial_state(self) -> np.ndarray:
        """Return the initial empty board state."""
        return np.zeros((self.board_size, self.board_size), dtype=int)
    
    def get_legal_moves(self, state: np.ndarray) -> List[Tuple[int, int]]:
        """Return a list of legal moves (empty cells) as (row, col) coordinates."""
        legal_moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if state[i, j] == 0:
                    legal_moves.append((i, j))
        return legal_moves
    
    def get_next_state(self, state: np.ndarray, move: Tuple[int, int]) -> np.ndarray:
        """
        Return the state after making the move.
        
        Args:
            state: Current board state
            move: Move to make as (row, col)
            
        Returns:
            New board state after the move
        """
        row, col = move
        # Determine whose turn it is by counting pieces
        pieces = np.sum(np.abs(state))
        player = 1 if pieces % 2 == 0 else -1
        
        # Create a copy of the state to avoid modifying the original
        new_state = state.copy()
        new_state[row, col] = player
        return new_state
    
    def is_terminal_state(self, state: np.ndarray) -> bool:
        """Check if the game is over (someone won or board is full)."""
        return self.get_winner(state) is not None
    
    def get_winner(self, state: np.ndarray) -> Optional[int]:
        """
        Return the winner of the game (1, -1, 0 for draw, None if game not over).
        """
        # Check rows
        for i in range(self.board_size):
            row_sum = np.sum(state[i, :])
            if abs(row_sum) == self.board_size:
                return 1 if row_sum > 0 else -1
                
        # Check columns
        for i in range(self.board_size):
            col_sum = np.sum(state[:, i])
            if abs(col_sum) == self.board_size:
                return 1 if col_sum > 0 else -1
                
        # Check diagonals
        diag1_sum = np.sum(np.diag(state))
        if abs(diag1_sum) == self.board_size:
            return 1 if diag1_sum > 0 else -1
            
        diag2_sum = np.sum(np.diag(np.fliplr(state)))
        if abs(diag2_sum) == self.board_size:
            return 1 if diag2_sum > 0 else -1
            
        # Check for draw (full board)
        if len(self.get_legal_moves(state)) == 0:
            return 0  # Draw
            
        # Game not over
        return None
    
    def evaluate(self, state: np.ndarray, player: int) -> float:
        """
        Evaluate the board from player's perspective.
        This is a simple heuristic for Tic-Tac-Toe that counts the number
        of potential winning lines.
        """
        score = 0
        opponent = -player
        
        # Check rows
        for i in range(self.board_size):
            row = state[i, :]
            if opponent not in row:
                score += 10 ** np.sum(row == player)
            if player not in row:
                score -= 10 ** np.sum(row == opponent)
                
        # Check columns
        for i in range(self.board_size):
            col = state[:, i]
            if opponent not in col:
                score += 10 ** np.sum(col == player)
            if player not in col:
                score -= 10 ** np.sum(col == opponent)
                
        # Check diagonals
        diag1 = np.diag(state)
        if opponent not in diag1:
            score += 10 ** np.sum(diag1 == player)
        if player not in diag1:
            score -= 10 ** np.sum(diag1 == opponent)
            
        diag2 = np.diag(np.fliplr(state))
        if opponent not in diag2:
            score += 10 ** np.sum(diag2 == player)
        if player not in diag2:
            score -= 10 ** np.sum(diag2 == opponent)
            
        return score
    
    def print_state(self, state: np.ndarray) -> None:
        """Print a human-readable representation of the board."""
        symbols = {0: ' ', 1: 'X', -1: 'O'}
        
        print("  " + " ".join(str(i) for i in range(self.board_size)))
        for i in range(self.board_size):
            print(f"{i} ", end="")
            for j in range(self.board_size):
                print(symbols[state[i, j]], end="")
                if j < self.board_size - 1:
                    print("|", end="")
            print()
            if i < self.board_size - 1:
                print("  " + "-".join(["-" for _ in range(self.board_size)]))