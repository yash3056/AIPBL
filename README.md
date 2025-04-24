# Tic-Tac-Toe AI Agent

This project implements an AI agent for Tic-Tac-Toe using the Minimax algorithm with Alpha-Beta pruning. The AI can play strategically and is designed to be unbeatable when set to sufficient search depth.

## Features

- Command-line interface to play Tic-Tac-Toe against the AI
- Implementation of Minimax algorithm with Alpha-Beta pruning for efficient decision making
- Adjustable AI difficulty through search depth parameter
- Option to play as first or second player
- Extensible architecture through the Game interface

## Requirements

- Python 3.6+
- NumPy library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/tictactoe-ai.git
cd tictactoe-ai
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game using the following command:

```bash
python main.py
```

### Command Line Options

- `--depth`: Set the maximum search depth for the AI (default: 5)
  ```bash
  python main.py --depth 3  # Easier AI
  python main.py --depth 7  # Harder AI
  ```

- `--second`: Let the AI play first, you play second
  ```bash
  python main.py --second
  ```

### Gameplay Instructions

1. The game board is displayed with row and column indices.
2. Enter your move in the format `row,col` (e.g., `1,2`).
3. The AI will respond with its move.
4. The game continues until someone wins or it's a draw.

## Project Structure

- `game.py`: Abstract base class defining the interface for games
- `minimax_agent.py`: Implementation of the Minimax algorithm with Alpha-Beta pruning
- `tictactoe.py`: Tic-Tac-Toe game implementation
- `main.py`: Command-line interface to play the game
- `requirements.txt`: List of Python dependencies

## How It Works

### Minimax Algorithm

The Minimax algorithm is a decision-making algorithm used in two-player games. It works by:

1. Exploring all possible game states up to a certain depth
2. Assigning scores to terminal states (win/loss/draw)
3. Propagating these scores back up the game tree, with:
   - The maximizing player choosing the move with the highest score
   - The minimizing player choosing the move with the lowest score

### Alpha-Beta Pruning

Alpha-Beta pruning is an optimization technique for the Minimax algorithm that reduces the number of nodes evaluated in the search tree by eliminating branches that don't need to be explored.

## Extending the Project

The architecture is designed to be extensible. You can:

1. Create new game implementations by extending the `Game` class
2. Modify the evaluation function in the `TicTacToe` class to change AI behavior
3. Experiment with different search algorithms in place of Minimax

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was inspired by the study of game theory and artificial intelligence
- Thanks to all contributors who have helped improve this project