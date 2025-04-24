import argparse
from typing import Optional, Any, List, Tuple
import time

from game import Game
from minimax_agent import MinimaxAgent
from tictactoe import TicTacToe


def play_game(game: Game, agent: MinimaxAgent, player_first: bool = True):
    """
    Play a game against the AI agent.
    
    Args:
        game: The game to play
        agent: The AI agent to play against
        player_first: Whether the human player goes first
    """
    state = game.get_initial_state()
    player_symbol = 1 if player_first else -1
    agent_symbol = -1 if player_first else 1
    
    # Announce game start
    print("\n===================================")
    print("  Game Started! You're playing as:", "X" if player_symbol == 1 else "O")
    print("===================================\n")
    
    # Main game loop
    current_player = 1  # Start with player 1 (X)
    
    while not game.is_terminal_state(state):
        # Display the current state
        game.print_state(state)
        
        if current_player == player_symbol:
            # Human player's turn
            print("\nYour turn!")
            move = get_player_move(game, state)
        else:
            # AI agent's turn
            print("\nAI is thinking...")
            start_time = time.time()
            move = agent.get_best_move(state, agent_symbol, verbose=True)
            end_time = time.time()
            print(f"AI chose move: {format_move(move)} (took {end_time - start_time:.2f} seconds)")
        
        # Make the move
        state = game.get_next_state(state, move)
        
        # Switch players
        current_player = -current_player
    
    # Game over, show final state
    game.print_state(state)
    
    # Announce winner
    winner = game.get_winner(state)
    if winner == player_symbol:
        print("\nCongratulations! You won!")
    elif winner == agent_symbol:
        print("\nThe AI won this time. Better luck next time!")
    else:
        print("\nIt's a draw!")


def get_player_move(game: Game, state: Any) -> Any:
    """Get a move from the human player."""
    legal_moves = game.get_legal_moves(state)
    
    if isinstance(game, TicTacToe):
        # Format for TicTacToe: row, col
        while True:
            try:
                move_input = input("Enter your move as 'row,col' (e.g., '1,2'): ")
                row, col = map(int, move_input.split(','))
                move = (row, col)
                
                if move in legal_moves:
                    return move
                else:
                    print("Invalid move! Please try again.")
            except (ValueError, IndexError):
                print("Invalid input format! Please use 'row,col'.")
    
    # Generic fallback
    print("Available moves:")
    for i, move in enumerate(legal_moves):
        print(f"{i+1}: {format_move(move)}")
        
    while True:
        try:
            choice = int(input(f"Enter move number (1-{len(legal_moves)}): "))
            if 1 <= choice <= len(legal_moves):
                return legal_moves[choice - 1]
            else:
                print("Invalid choice! Please try again.")
        except ValueError:
            print("Please enter a number!")


def format_move(move: Any) -> str:
    """Format a move for display to the user."""
    if isinstance(move, tuple):
        # Tic-tac-toe move format: (row, col)
        row, col = move
        return f"({row}, {col})"
    return str(move)


def main():
    """Main entry point for the game."""
    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe against a Minimax AI agent.")
    parser.add_argument("--depth", type=int, default=5,
                        help="Maximum search depth for the AI (default: 5)")
    parser.add_argument("--second", action="store_true",
                        help="Let AI play first, you play second")
    
    args = parser.parse_args()
    
    # Create the game
    game = TicTacToe()
    print("\nStarting Tic-Tac-Toe game against AI...")
    
    # Create the AI agent
    agent = MinimaxAgent(game, max_depth=args.depth)
    
    # Play the game
    player_first = not args.second
    play_game(game, agent, player_first=player_first)


if __name__ == "__main__":
    main()