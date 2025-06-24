import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants for window size and game layout
WIDTH, HEIGHT = 600, 660  # 600 for game board, extra 60 for buttons
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
BUTTON_HEIGHT = 60  # Height of the Restart and message area

# Game drawing constants
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4  # Padding for the cross drawing

# Color definitions (RGB)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BUTTON_COLOR = (84, 84, 84)
TEXT_COLOR = (255, 255, 255)
WIN_LINE_COLOR = (255, 0, 0)

# Fonts for text display
font = pygame.font.SysFont(None, 36)
winner_font = pygame.font.SysFont(None, 40)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe - AI vs Player')

# Game variables
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]  # 3x3 board initialized with None
PLAYER = None  # Will hold 'X' or 'O' for player
AI = None      # Will hold 'X' or 'O' for AI
winner_text = ""  # Message to show winner/draw
game_over = False
win_line = None  # Coordinates of winning line to be drawn
game_started = False  # Game state tracker

# Draws the grid lines for the board
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)  # Horizontal
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, SQUARE_SIZE * BOARD_ROWS), LINE_WIDTH)  # Vertical

# Draws Xs and Os on the board based on the board matrix
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                          row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

# Draws the red winning line based on coordinates
def draw_win_line(start, end):
    pygame.draw.line(screen, WIN_LINE_COLOR, start, end, 10)

# Places player's symbol in the board matrix
def mark_square(row, col, player):
    board[row][col] = player

# Checks if a cell is empty
def available_square(row, col):
    return board[row][col] is None

# Checks if the board is full (for draw condition)
def is_full():
    return all(all(cell is not None for cell in row) for row in board)

# Checks if a player has won and returns coordinates to draw winning line
def check_winner(player):
    # Horizontal win
    for row in range(BOARD_ROWS):
        if board[row] == [player] * 3:
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            return ((0, y), (WIDTH, y))

    # Vertical win
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            return ((x, 0), (x, SQUARE_SIZE * BOARD_ROWS))

    # Diagonal wins
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return ((0, 0), (WIDTH, SQUARE_SIZE * BOARD_ROWS))

    if all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return ((WIDTH, 0), (0, SQUARE_SIZE * BOARD_ROWS))

    return None

# Minimax algorithm for AI move selection
def minimax(depth, is_maximizing):
    if check_winner(AI):
        return 1
    if check_winner(PLAYER):
        return -1
    if is_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = AI
                    score = minimax(depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = PLAYER
                    score = minimax(depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score

# Finds the best move for AI using Minimax
def best_move():
    best_score = -math.inf
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = AI
                score = minimax(0, False)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

# Resets the game state
def restart():
    global board, game_over, winner_text, win_line, game_started
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    winner_text = ""
    win_line = None
    game_started = False

# Draws the Restart button and winner/draw message
def draw_buttons():
    # Restart Button
    pygame.draw.rect(screen, BUTTON_COLOR, (0, HEIGHT - BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT))
    text = font.render("Restart", True, TEXT_COLOR)
    screen.blit(text, text.get_rect(center=(WIDTH // 4, HEIGHT - BUTTON_HEIGHT // 2)))

    # Winner/Draw Text
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2, HEIGHT - BUTTON_HEIGHT, WIDTH // 2, BUTTON_HEIGHT))
    label = winner_font.render(winner_text, True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=(3 * WIDTH // 4, HEIGHT - BUTTON_HEIGHT // 2)))

# Shows the start screen where user picks X or O
def draw_start_screen():
    screen.fill(BG_COLOR)
    title = winner_font.render("Choose Your Symbol", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

    # X Button
    pygame.draw.rect(screen, BUTTON_COLOR, (150, 200, 120, 80))
    x_text = font.render("Play as X", True, TEXT_COLOR)
    screen.blit(x_text, (150 + 10, 200 + 20))

    # O Button
    pygame.draw.rect(screen, BUTTON_COLOR, (330, 200, 120, 80))
    o_text = font.render("Play as O", True, TEXT_COLOR)
    screen.blit(o_text, (330 + 10, 200 + 20))

    pygame.display.update()

# Main Game Loop
while True:
    if not game_started:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 150 <= mx <= 270 and 200 <= my <= 280:
                    PLAYER, AI = 'X', 'O'
                    game_started = True
                elif 330 <= mx <= 450 and 200 <= my <= 280:
                    PLAYER, AI = 'O', 'X'
                    game_started = True

                if game_started:
                    screen.fill(BG_COLOR)
                    draw_lines()
                    draw_buttons()
                    # If AI goes first
                    if PLAYER == 'O':
                        row, col = best_move()
                        mark_square(row, col, AI)
                        draw_figures()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Handle Restart button
                if HEIGHT - BUTTON_HEIGHT <= mouse_y <= HEIGHT and mouse_x < WIDTH // 2:
                    restart()
                elif not game_over and mouse_y < HEIGHT - BUTTON_HEIGHT:
                    x_pos = mouse_x // SQUARE_SIZE
                    y_pos = mouse_y // SQUARE_SIZE

                    if available_square(y_pos, x_pos):
                        mark_square(y_pos, x_pos, PLAYER)
                        draw_figures()

                        # Check if player wins
                        result = check_winner(PLAYER)
                        if result:
                            win_line = result
                            winner_text = "Player wins!"
                            game_over = True
                        elif is_full():
                            winner_text = "Draw!"
                            game_over = True
                        else:
                            # AI Move
                            row, col = best_move()
                            if row is not None:
                                mark_square(row, col, AI)
                                draw_figures()
                                result = check_winner(AI)
                                if result:
                                    win_line = result
                                    winner_text = "AI wins!"
                                    game_over = True
                                elif is_full():
                                    winner_text = "Draw!"
                                    game_over = True

        # If game is over and win line exists, draw it
        if game_over:
            if win_line:
                draw_win_line(*win_line)

        draw_buttons()
        pygame.display.update()
