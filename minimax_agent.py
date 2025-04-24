from typing import Any, Tuple, Optional
import time
from game import Game

class MinimaxAgent:
    """
    AI agent that uses Minimax algorithm with Alpha-Beta pruning to decide moves.
    """
    
    def __init__(self, game: Game, max_depth: int = 5):
        """
        Initialize the Minimax agent.
        
        Args:
            game: The game the agent will play
            max_depth: Maximum search depth for the minimax algorithm
        """
        self.game = game
        self.max_depth = max_depth
        self.nodes_explored = 0
    
    def get_best_move(self, state: Any, player: int, verbose: bool = False) -> Any:
        """
        Find the best move for the player in the given state.
        
        Args:
            state: Current game state
            player: Current player (1 or -1)
            verbose: Whether to print stats about the search
            
        Returns:
            The best move found
        """
        self.nodes_explored = 0
        start_time = time.time()
        
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        for move in self.game.get_legal_moves(state):
            next_state = self.game.get_next_state(state, move)
            value = self._min_value(next_state, player, 1, alpha, beta)
            
            if value > best_value:
                best_value = value
                best_move = move
            
            alpha = max(alpha, best_value)
        
        end_time = time.time()
        
        if verbose:
            print(f"Minimax with Alpha-Beta pruning stats:")
            print(f"Time taken: {end_time - start_time:.3f} seconds")
            print(f"Nodes explored: {self.nodes_explored}")
            print(f"Best move value: {best_value}")
            
        return best_move
    
    def _max_value(self, state: Any, player: int, depth: int, alpha: float, beta: float) -> float:
        """Maximizing player's turn in minimax algorithm."""
        self.nodes_explored += 1
        
        if self.game.is_terminal_state(state):
            winner = self.game.get_winner(state)
            if winner == player:
                return 1000.0
            elif winner == 0:  # Draw
                return 0.0
            else:  # Opponent won
                return -1000.0
                
        if depth >= self.max_depth:
            return self.game.evaluate(state, player)
            
        value = float('-inf')
        
        for move in self.game.get_legal_moves(state):
            next_state = self.game.get_next_state(state, move)
            value = max(value, self._min_value(next_state, player, depth + 1, alpha, beta))
            
            if value >= beta:
                return value  # Beta cutoff
            
            alpha = max(alpha, value)
            
        return value
    
    def _min_value(self, state: Any, player: int, depth: int, alpha: float, beta: float) -> float:
        """Minimizing player's turn in minimax algorithm."""
        self.nodes_explored += 1
        
        if self.game.is_terminal_state(state):
            winner = self.game.get_winner(state)
            if winner == player:
                return 1000.0
            elif winner == 0:  # Draw
                return 0.0
            else:  # Opponent won
                return -1000.0
                
        if depth >= self.max_depth:
            return self.game.evaluate(state, player)
            
        value = float('inf')
        
        for move in self.game.get_legal_moves(state):
            next_state = self.game.get_next_state(state, move)
            value = min(value, self._max_value(next_state, player, depth + 1, alpha, beta))
            
            if value <= alpha:
                return value  # Alpha cutoff
            
            beta = min(beta, value)
            
        return value