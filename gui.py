import pygame
import sys
import numpy as np
import time
from tictactoe import TicTacToe
from minimax_agent import MinimaxAgent

class TicTacToeGUI:
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    BG_COLOR = (245, 245, 245)
    
    # Dimensions
    WIDTH = 600
    HEIGHT = 600
    LINE_WIDTH = 15
    BOARD_ROWS = 3
    BOARD_COLS = 3
    SQUARE_SIZE = WIDTH // BOARD_COLS
    CIRCLE_RADIUS = SQUARE_SIZE // 3
    CIRCLE_WIDTH = 15
    CROSS_WIDTH = 25
    SPACE = SQUARE_SIZE // 4
    
    def __init__(self, ai_depth=5, player_first=True):
        """
        Initialize the GUI for Tic-Tac-Toe
        
        Args:
            ai_depth: Depth for the Minimax algorithm
            player_first: Whether the human player goes first
        """
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Tic Tac Toe with Minimax AI')
        self.screen.fill(self.BG_COLOR)
        
        # Game state
        self.game = TicTacToe()
        self.state = self.game.get_initial_state()
        self.agent = MinimaxAgent(self.game, max_depth=ai_depth)
        
        # Player setup
        self.player_symbol = 1 if player_first else -1
        self.ai_symbol = -1 if player_first else 1
        self.current_player = 1  # X always starts
        
        # Game status
        self.game_over = False
        self.winner = None
        
        # Draw initial board
        self.draw_lines()
        
        # AI makes first move if player is second
        if not player_first:
            self.ai_make_move()
    
    def draw_lines(self):
        """Draw the board lines"""
        # Horizontal lines
        for i in range(1, self.BOARD_ROWS):
            pygame.draw.line(
                self.screen, self.BLACK, 
                (0, i * self.SQUARE_SIZE), 
                (self.WIDTH, i * self.SQUARE_SIZE), 
                self.LINE_WIDTH
            )
        
        # Vertical lines
        for i in range(1, self.BOARD_COLS):
            pygame.draw.line(
                self.screen, self.BLACK, 
                (i * self.SQUARE_SIZE, 0), 
                (i * self.SQUARE_SIZE, self.HEIGHT), 
                self.LINE_WIDTH
            )
    
    def draw_figures(self):
        """Draw X and O on the board based on the game state"""
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                center_x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                center_y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                
                if self.state[row, col] == 1:  # X
                    # Draw X
                    pygame.draw.line(
                        self.screen, self.RED,
                        (center_x - self.SPACE, center_y - self.SPACE),
                        (center_x + self.SPACE, center_y + self.SPACE),
                        self.CROSS_WIDTH
                    )
                    pygame.draw.line(
                        self.screen, self.RED,
                        (center_x + self.SPACE, center_y - self.SPACE),
                        (center_x - self.SPACE, center_y + self.SPACE),
                        self.CROSS_WIDTH
                    )
                elif self.state[row, col] == -1:  # O
                    # Draw O
                    pygame.draw.circle(
                        self.screen, self.BLUE,
                        (center_x, center_y),
                        self.CIRCLE_RADIUS,
                        self.CIRCLE_WIDTH
                    )
    
    def handle_click(self, row, col):
        """Handle player's click on a cell"""
        if not self.game_over and self.current_player == self.player_symbol:
            # Check if the cell is empty
            if self.state[row, col] == 0:
                # Make the move
                self.state = self.game.get_next_state(self.state, (row, col))
                self.current_player = -self.current_player
                
                # Check if game is over
                self.check_game_over()
                
                # Draw the updated board
                self.draw_figures()
                
                # AI's turn if game is not over
                if not self.game_over:
                    self.ai_make_move()
    
    def ai_make_move(self):
        """Let the AI make a move"""
        # Add a small delay to make the AI's move visible
        pygame.display.update()
        time.sleep(0.5)
        
        # AI makes its move
        move = self.agent.get_best_move(self.state, self.ai_symbol)
        self.state = self.game.get_next_state(self.state, move)
        self.current_player = -self.current_player
        
        # Check if game is over
        self.check_game_over()
        
        # Draw the updated board
        self.draw_figures()
    
    def check_game_over(self):
        """Check if the game is over and update game status"""
        if self.game.is_terminal_state(self.state):
            self.game_over = True
            self.winner = self.game.get_winner(self.state)
            self.display_result()
    
    def display_result(self):
        """Display the game result"""
        font = pygame.font.Font(None, 40)
        
        if self.winner == self.player_symbol:
            text = font.render("You Won!", True, self.GREEN)
        elif self.winner == self.ai_symbol:
            text = font.render("AI Won!", True, self.RED)
        else:
            text = font.render("It's a Draw!", True, self.BLACK)
        
        # Create a semi-transparent background for the text
        overlay = pygame.Surface((self.WIDTH, 80))
        overlay.set_alpha(180)
        overlay.fill(self.WHITE)
        self.screen.blit(overlay, (0, self.HEIGHT // 2 - 40))
        
        # Display the text
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        # Display restart instructions
        restart_font = pygame.font.Font(None, 30)
        restart_text = restart_font.render("Press R to restart or Q to quit", True, self.BLACK)
        restart_rect = restart_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 30))
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self, player_first=None):
        """Restart the game"""
        # Reset the game state
        self.state = self.game.get_initial_state()
        self.current_player = 1  # X always starts
        
        # Update player symbols if specified
        if player_first is not None:
            self.player_symbol = 1 if player_first else -1
            self.ai_symbol = -1 if player_first else 1
        
        # Reset game status
        self.game_over = False
        self.winner = None
        
        # Clear the screen and redraw the board
        self.screen.fill(self.BG_COLOR)
        self.draw_lines()
        
        # AI makes first move if player is second
        if self.player_symbol == -1:
            self.ai_make_move()
    
    def run(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and self.current_player == self.player_symbol:
                    mouseX, mouseY = event.pos
                    clicked_row = mouseY // self.SQUARE_SIZE
                    clicked_col = mouseX // self.SQUARE_SIZE
                    
                    if 0 <= clicked_row < self.BOARD_ROWS and 0 <= clicked_col < self.BOARD_COLS:
                        self.handle_click(clicked_row, clicked_col)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game
                        self.restart_game()
                    elif event.key == pygame.K_1:  # Play as X (first)
                        self.restart_game(True)
                    elif event.key == pygame.K_2:  # Play as O (second)
                        self.restart_game(False)
                    elif event.key == pygame.K_q:  # Quit game
                        pygame.quit()
                        sys.exit()
            
            # Update display
            pygame.display.update()


def main():
    """Main entry point for the GUI game."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe with GUI against a Minimax AI agent.")
    parser.add_argument("--depth", type=int, default=5,
                        help="Maximum search depth for the AI (default: 5)")
    parser.add_argument("--second", action="store_true",
                        help="Let AI play first, you play second")
    
    args = parser.parse_args()
    
    # Start the game
    print("\nStarting Tic-Tac-Toe with GUI...")
    print("Controls:")
    print("- Click on a cell to make a move")
    print("- Press R to restart the game")
    print("- Press 1 to play as X (first player)")
    print("- Press 2 to play as O (second player)")
    print("- Press Q to quit the game")
    
    game_gui = TicTacToeGUI(ai_depth=args.depth, player_first=not args.second)
    game_gui.run()


if __name__ == "__main__":
    main()