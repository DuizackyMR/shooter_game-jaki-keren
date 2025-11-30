import pygame, random

pygame.init()

# -------------------------
# GAME SETTINGS
# -------------------------
WIDTH, HEIGHT = 320, 640
BLOCK = 32
COLS, ROWS = WIDTH // BLOCK, HEIGHT // BLOCK
screen = pygame.display.set_mode((WIDTH + 160, HEIGHT))
pygame.display.set_caption("TETRIS FULL")

FONT = pygame.font.SysFont("consolas", 24)

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
]

shapes = [
    [[1,1,1,1]],
    [[1,1],[1,1]],
    [[0,1,0],[1,1,1]],
    [[1,0,0],[1,1,1]],
    [[0,0,1],[1,1,1]],
    [[1,1,0],[0,1,1]],
    [[0,1,1],[1,1,0]],
]


# -------------------------
# PIECE CLASS
# -------------------------
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.randint(1, len(colors)-1)

    @property
    def rotated(self):
        return [
            [self.shape[y][x] for y in range(len(self.shape))]
            for x in range(len(self.shape[0]) - 1, -1, -1)
        ]


# -------------------------
# FUNCTIONS
# -------------------------
def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]


def valid(piece, board):
    for i, row in enumerate(piece.shape):
        for j, val in enumerate(row):
            if val:
                px = piece.x + j
                py = piece.y + i

                if px < 0 or px >= COLS or py >= ROWS:
                    return False
                if py >= 0 and board[py][px]:
                    return False
    return True


def lock_piece(piece, board):
    for i, row in enumerate(piece.shape):
        for j, val in enumerate(row):
            if val:
                board[piece.y + i][piece.x + j] = piece.color


def clear_rows(board):
    cleared = 0
    for i in range(ROWS-1, -1, -1):
        if 0 not in board[i]:
            cleared += 1
            del board[i]
            board.insert(0, [0]*COLS)
    return cleared


def draw_board(board):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, colors[board[y][x]],
                             (x*BLOCK, y*BLOCK, BLOCK, BLOCK))
            pygame.draw.rect(screen, (60,60,60),
                             (x*BLOCK, y*BLOCK, BLOCK, BLOCK), 1)


def draw_piece(piece):
    for i, row in enumerate(piece.shape):
        for j, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, colors[piece.color],
                                 ((piece.x+j)*BLOCK, (piece.y+i)*BLOCK, BLOCK, BLOCK))


def draw_next(next_shape, color):
    label = FONT.render("NEXT:", True, (255,255,255))
    screen.blit(label, (WIDTH + 20, 20))
    for i, row in enumerate(next_shape):
        for j, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, colors[color],
                                 (WIDTH + 40 + j*BLOCK, 60 + i*BLOCK, BLOCK, BLOCK))


def draw_hold(hold_shape, color):
    label = FONT.render("HOLD:", True, (255,255,255))
    screen.blit(label, (WIDTH + 20, 180))
    if hold_shape:
        for i, row in enumerate(hold_shape):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, colors[color],
                                     (WIDTH + 40 + j*BLOCK, 220 + i*BLOCK, BLOCK, BLOCK))


# -------------------------
# GAME OVER MENU
# -------------------------
def game_over_screen():
    screen.fill((0, 0, 0))
    
    over = FONT.render("GAME OVER", True, (255, 50, 50))
    restart = FONT.render("R = Retry", True, (255, 255, 255))
    quit_game = FONT.render("Q = Quit", True, (255, 255, 255))

    screen.blit(over, (WIDTH//2 - 40, HEIGHT//2 - 40))
    screen.blit(restart, (WIDTH//2 - 40, HEIGHT//2))
    screen.blit(quit_game, (WIDTH//2 - 40, HEIGHT//2 + 40))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True   # restart
                if event.key == pygame.K_q:
                    return False  # quit


# -------------------------
# MAIN GAME
# -------------------------
def main():
    board = create_board()
    clock = pygame.time.Clock()

    current = Piece(COLS//2 - 2, 0, random.choice(shapes))
    next_piece = Piece(0,0, random.choice(shapes))
    hold_piece = None
    hold_used = False

    fall_time = 0
    fall_speed = 450
    score = 0

    running = True
    while running:
        dt = clock.tick(60)
        fall_time += dt

        if fall_time >= fall_speed:
            current.y += 1
            if not valid(current, board):
                current.y -= 1
                lock_piece(current, board)

                lines = clear_rows(board)
                if lines == 1: score += 100
                elif lines == 2: score += 300
                elif lines == 3: score += 500
                elif lines == 4: score += 800

                current = Piece(COLS//2 - 2, 0, next_piece.shape)
                current.color = next_piece.color
                next_piece = Piece(0,0, random.choice(shapes))
                hold_used = False

                if not valid(current, board):
                    running = False

            fall_time = 0

        # CONTROLS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current.x -= 1
                    if not valid(current, board): current.x += 1

                if event.key == pygame.K_RIGHT:
                    current.x += 1
                    if not valid(current, board): current.x -= 1

                if event.key == pygame.K_DOWN:
                    current.y += 1
                    score += 1
                    if not valid(current, board): current.y -= 1

                if event.key == pygame.K_SPACE:
                    while valid(current, board):
                        current.y += 1
                    current.y -= 1
                    score += 2

                    lock_piece(current, board)
                    lines = clear_rows(board)
                    if lines: score += lines * 200

                    current = Piece(COLS//2 - 2, 0, next_piece.shape)
                    current.color = next_piece.color
                    next_piece = Piece(0,0, random.choice(shapes))
                    hold_used = False

                if event.key == pygame.K_UP:
                    old = current.shape
                    current.shape = current.rotated
                    if not valid(current, board):
                        current.shape = old

                if event.key == pygame.K_c and not hold_used:
                    if hold_piece is None:
                        hold_piece = Piece(0, 0, current.shape)
                        hold_piece.color = current.color

                        current = Piece(COLS//2 - 2, 0, next_piece.shape)
                        current.color = next_piece.color
                        next_piece = Piece(0,0, random.choice(shapes))

                    else:
                        hold_piece.shape, current.shape = current.shape, hold_piece.shape
                        hold_piece.color, current.color = current.color, hold_piece.color
                        current.x, current.y = COLS//2 - 2, 0

                    hold_used = True

        # DRAW
        screen.fill((0,0,0))
        draw_board(board)
        draw_piece(current)
        draw_next(next_piece.shape, next_piece.color)
        draw_hold(hold_piece.shape if hold_piece else None,
                  hold_piece.color if hold_piece else 0)

        score_txt = FONT.render(f"SCORE: {score}", True, (255,255,255))
        screen.blit(score_txt, (WIDTH + 20, 350))

        pygame.display.update()

    # GAME OVER MENU
    if game_over_screen():
        main()   # restart
    else:
        pygame.quit()


if __name__ == "__main__":
    main()