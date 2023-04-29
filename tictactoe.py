import pygame
import random

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BOARD_SIZE = 3
BOARD_SPACING = 80
BOARD_X = (SCREEN_WIDTH - BOARD_SIZE * BOARD_SPACING) / 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_SIZE * BOARD_SPACING) / 2
FONT_SIZE = 64
SHAKE_TIME = 0.5
SHAKE_MAGNITUDE = 10
SHAKE_FREQUENCY = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exo - Noughts and Crosses")
FONT = pygame.font.SysFont(None, FONT_SIZE)

# Initialize board
BOARD = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Functions
def draw_board():
    screen.fill(BLACK)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            rect = pygame.Rect(BOARD_X + x * BOARD_SPACING, BOARD_Y + y * BOARD_SPACING, BOARD_SPACING, BOARD_SPACING)
            pygame.draw.rect(screen, WHITE, rect, 2)
            if BOARD[x][y] is not None:
                text_surface = FONT.render(BOARD[x][y], True, WHITE)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
    pygame.display.update()

def check_winner():
    # Check rows
    for y in range(BOARD_SIZE):
        if all(BOARD[x][y] == BOARD[0][y] and BOARD[x][y] is not None for x in range(BOARD_SIZE)):
            return BOARD[0][y]
    # Check columns
    for x in range(BOARD_SIZE):
        if all(BOARD[x][y] == BOARD[x][0] and BOARD[x][y] is not None for y in range(BOARD_SIZE)):
            return BOARD[x][0]
    # Check diagonal
    if all(BOARD[x][x] == BOARD[0][0] and BOARD[x][x] is not None for x in range(BOARD_SIZE)):
        return BOARD[0][0]
    if all(BOARD[x][BOARD_SIZE-1-x] == BOARD[0][BOARD_SIZE-1] and BOARD[x][BOARD_SIZE-1-x] is not None for x in range(BOARD_SIZE)):
        return BOARD[0][BOARD_SIZE-1]
    # Check for tie
    if all(BOARD[x][y] is not None for x in range(BOARD_SIZE) for y in range(BOARD_SIZE)):
        return "Tie"
    # No winner
    return None

def make_move(x, y, player):
    BOARD[x][y] = player
    draw_board()
    winner = check_winner()
    if winner is not None:
        if winner == "Tie":
            message = "It's a tie!"
        else:
            message = f"{winner} wins!"
        text_surface = FONT.render(message, True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)
        reset_board()
    else:
        if player == "X":
            player = "O"
        else:
            player = "X"


def reset_board():
  global BOARD
  BOARD = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
  draw_board()

def shake_screen():
    start_time = pygame.time.get_ticks() / 1000
    while pygame.time.get_ticks() / 1000 - start_time < SHAKE_TIME:
        dx = random.randint(-SHAKE_MAGNITUDE, SHAKE_MAGNITUDE)
        dy = random.randint(-SHAKE_MAGNITUDE, SHAKE_MAGNITUDE)
        screen.fill(BLACK)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                rect = pygame.Rect(BOARD_X + x * BOARD_SPACING + dx, BOARD_Y + y * BOARD_SPACING + dy, BOARD_SPACING, BOARD_SPACING)
                pygame.draw.rect(screen, WHITE, rect, 2)
                if BOARD[x][y] is not None:
                    text_surface = FONT.render(BOARD[x][y], True, WHITE)
                    text_rect = text_surface.get_rect(center=rect.center)
                    screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.wait(1000 // SHAKE_FREQUENCY)
    draw_board()

# Initialize the selected cell position
selected_x = 0
selected_y = 0

# Main loop
reset_board()
player = "X"  # player "X" goes first
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            # Handle arrow key controls to select the place to put nought or cross
            if event.key == pygame.K_UP:
                selected_y = (selected_y - 1) % BOARD_SIZE
                draw_board()
            elif event.key == pygame.K_DOWN:
                selected_y = (selected_y + 1) % BOARD_SIZE
                draw_board()
            elif event.key == pygame.K_LEFT:
                selected_x = (selected_x - 1) % BOARD_SIZE
                draw_board()
            elif event.key == pygame.K_RIGHT:
                selected_x = (selected_x + 1) % BOARD_SIZE
                draw_board()
            # Handle space bar or enter key press to place nought or cross
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if BOARD[selected_x][selected_y] is None:  # Check if the cell is empty
                    BOARD[selected_x][selected_y] = player  # Place nought or cross in the cell
                    draw_board()  # Redraw the board with the new move
                    winner = check_winner()  # Check if there is a winner or a tie
                    if winner is not None:  # If there is a winner or a tie
                        if winner == "Tie":
                            message = "It's a tie!"
                        else:
                            message = f"{winner} wins!"
                        # Display the winner or tie message
                        text_surface = FONT.render(message, True, RED)
                        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                        screen.blit(text_surface, text_rect)
                        pygame.display.update()
                        pygame.time.wait(2000)  # Wait for 2 seconds
                        reset_board()  # Reset the board to start a new game
                    else:  # If the game is not over yet
                        if player == "X":
                            player = "O"  # Switch to the other player
                        else:
                            player = "X"
                else:  # If the cell is not empty
                    shake_screen()  # Shake the screen to indicate an invalid move
    # Draw the board and highlight the selected cell
    draw_board()
    pygame.draw.rect(screen, RED, pygame.Rect(BOARD_X + selected_x * BOARD_SPACING, BOARD_Y + selected_y * BOARD_SPACING, BOARD_SPACING, BOARD_SPACING), 5)
    pygame.display.update()
