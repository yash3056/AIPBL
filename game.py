from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Any


class Game(ABC):
    """Abstract base class for games that can be played by the AI agent."""
    
    @abstractmethod
    def get_initial_state(self) -> Any:
        """Return the initial state of the game."""
        pass
    
    @abstractmethod
    def get_legal_moves(self, state: Any) -> List[Any]:
        """Return a list of legal moves from the given state."""
        pass
    
    @abstractmethod
    def get_next_state(self, state: Any, move: Any) -> Any:
        """Return the state that results from making the move in the given state."""
        pass
    
    @abstractmethod
    def is_terminal_state(self, state: Any) -> bool:
        """Return True if the given state is terminal (game over)."""
        pass
    
    @abstractmethod
    def get_winner(self, state: Any) -> Optional[int]:
        """Return the winner of the game in the given state (1 for player 1, -1 for player 2, 0 for draw, None if game not over)."""
        pass
    
    @abstractmethod
    def evaluate(self, state: Any, player: int) -> float:
        """Return a heuristic evaluation of the given state from the perspective of the specified player."""
        pass
    
    @abstractmethod
    def print_state(self, state: Any) -> None:
        """Print a human-readable representation of the state."""
        pass