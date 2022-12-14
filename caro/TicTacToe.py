import sys
import pygame
import pickle

'''
PREPARE
'''
pygame.init()
game_font = pygame.font.Font(pygame.font.get_default_font(), 34)
BOARD_SIZE = 15
cell_size = 40
win_streak = 5
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)
size = BOARD_SIZE * cell_size, BOARD_SIZE * cell_size
turn = 0
screen = pygame.display.set_mode(size)

with open("config.xor_value", 'rb') as rf:
    xor_val_data = dict(pickle.load(rf))
    rf.close()
with open("config.random_value", 'rb') as rf:
    xor_val = pickle.load(rf)
    rf.close()
board_xor = int(0)
cell_val = [[0 for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
cell_pos = [[0 for i in range(BOARD_SIZE - 1)] for j in range(BOARD_SIZE * BOARD_SIZE)]
for i in range(BOARD_SIZE):
    for j in range(BOARD_SIZE):
        id = i * BOARD_SIZE + j
        cell_pos[id][0] = j * cell_size
        cell_pos[id][1] = i * cell_size
just_check = []

'''
GAME UI
'''


def check_Cell(_mouse_Cell):
    global board_xor
    if len(_mouse_Cell) == 0:
        return False
    if cell_val[_mouse_Cell[1]][_mouse_Cell[0]] == 0:
        cell_val[_mouse_Cell[1]][_mouse_Cell[0]] = turn + 1
        board_xor = board_xor ^ xor_val[_mouse_Cell[1]][_mouse_Cell[0]][2]
        just_check = [_mouse_Cell[1], _mouse_Cell[0]]
        return True
    return False


def check(x, y, ix, iy):
    for i in range(win_streak - 1):
        val = cell_val[y][x]
        if val == 0:
            return False
        x = x + ix
        y = y + iy
        if x <= 0 or x >= BOARD_SIZE or y <= 0 or y >= BOARD_SIZE:
            return False
        if val != cell_val[y][x]:
            return False
    return True


def Check_winner():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if check(i, j, 1, 0) or check(i, j, 0, 1) or check(i, j, 1, 1) or check(i, j, -1, 1):
                return True
    return False


def Check_draw():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if cell_val[i][j] == 0:
                return False
    return True


def draw_screen():
    screen.fill('white')
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            id = i * BOARD_SIZE + j
            COLOR = 'lightblue'
            if [i, j] == just_check:
                COLOR = 'yellow'
            r = pygame.Rect(cell_pos[id][0], cell_pos[id][1], cell_size, cell_size)
            pygame.draw.rect(surface=screen, rect=r, color=COLOR)
            r = pygame.Rect(cell_pos[id][0] + 1, cell_pos[id][1] + 1, cell_size - 2, cell_size - 2)
            pygame.draw.rect(surface=screen, rect=r, color='white')

            if cell_val[i][j] == 1:
                text_surface = game_font.render("X", True, WHITE, BLACK)
                screen.blit(text_surface, (cell_pos[id][0] + 8, cell_pos[id][1] + 4))
            if cell_val[i][j] == 2:
                text_surface = game_font.render("O", True, WHITE, BLACK)
                screen.blit(text_surface, (cell_pos[id][0] + 8, cell_pos[id][1] + 4))
    if turn == 3:
        text_surface = game_font.render("Winner Found", True, WHITE, BLACK)
        screen.blit(text_surface, (size[0] // 3, 0))
    if turn == 4:
        text_surface = game_font.render("It's a Draw", True, WHITE, BLACK)
        screen.blit(text_surface, (size[0] // 3, 0))
    pygame.display.flip()


'''
AI CODE
'''
dx = [0, 1, 1, -1]
dy = [1, 0, 1, 1]

ai_score = {tuple([1, 1, 1, 0, 0]): 50,
            tuple([0, 0, 1, 1, 1]): 50,
            tuple([0, 1, 1, 1, 0]): 500,
            tuple([0, 1, 0, 1, 1, 0]): 500000,
            tuple([0, 1, 1, 0, 1, 0]): 500000,
            tuple([0, 1, 1, 1, 1]): 500000000,
            tuple([1, 0, 1, 1, 1]): 500000000,
            tuple([1, 1, 0, 1, 1]): 500000000,
            tuple([1, 1, 1, 0, 1]): 500000000,
            tuple([1, 1, 1, 1, 0]): 500000000,
            tuple([0, 1, 1, 1, 1, 0]): 5000000000,
            tuple([1, 1, 1, 1, 1]): 5000000000000}

player_score = {tuple([2, 2, 2, 0, 0]): 50,
                tuple([0, 0, 2, 2, 2]): 50,
                tuple([0, 2, 2, 2, 0]): 500,
                tuple([0, 2, 0, 2, 2, 0]): 500000,
                tuple([0, 2, 2, 0, 2, 0]): 500000,
                tuple([0, 2, 2, 2, 2]): 500000000,
                tuple([2, 0, 2, 2, 2]): 500000000,
                tuple([2, 2, 0, 2, 2]): 500000000,
                tuple([2, 2, 2, 0, 2]): 500000000,
                tuple([2, 2, 2, 2, 0]): 500000000,
                tuple([0, 2, 2, 2, 2, 0]): 5000000000,
                tuple([2, 2, 2, 2, 2]): 5000000000000}

adjx = [-1, -1, -1, 0, 0, 1, 1, 1]
adjy = [-1, 0, 1, -1, 1, -1, 0, 1]

cell = cell_val.copy()




class AI:
    def __init__(self, _turn):
        self.depth = 2
        self.turn = _turn

    def check_win(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if cell[i][j] == 0: continue
                for dir in range(4):
                    nx = i
                    ny = j
                    ch = True
                    for k in range(win_streak - 1):
                        nx = nx + dx[dir]
                        ny = ny + dy[dir]
                        if nx == 0 or nx == BOARD_SIZE or ny == 0 or ny == BOARD_SIZE or cell[nx][ny] != cell[i][j]:
                            ch = False
                            break
                    if ch:
                        return True
        return False

    def get_score(self, x, y, le):
        score = 0
        for dir in range(4):
            st = []
            st.append(cell[x][y])
            nx = x
            ny = y
            for i in range(le - 1):
                nx = nx + dx[dir]
                ny = ny + dy[dir]
                if nx == 0 or nx == BOARD_SIZE or ny == 0 or ny == BOARD_SIZE:
                    break
                else:
                    st.append(cell[nx][ny])
            st = tuple(st)
            if st in ai_score.keys():
                score += ai_score[st]

            if st in player_score.keys():
                score -= player_score[st]
        return score

    def cal(self):
        score = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                s5 = self.get_score(i, j, 5)
                s6 = self.get_score(i, j, 6)
                score += s5 + s6
        return score

    def minimax(self, _depth, alpha, beta, maximize):
        global board_xor
        if _depth == 0 or self.check_win():
            return [self.cal(), [-1, -1]]

        mask = str(board_xor) + str(_depth)
        if mask in xor_val_data.keys():
            return xor_val_data.get(mask)

        if maximize:
            move = []
            C_val = -1000000000000000
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if cell[i][j] == 0: continue
                    for dir in range(8):
                        nx = i + adjx[dir]
                        ny = j + adjy[dir]
                        if nx == 0 or nx == BOARD_SIZE or ny == 0 or ny == BOARD_SIZE or cell[nx][ny] != 0: continue
                        cell[nx][ny] = 1
                        board_xor = board_xor ^ xor_val[nx][ny][1]
                        val = self.minimax(_depth - 1, alpha, beta, False)
                        if C_val < val[0]:
                            C_val = val[0]
                            move = [nx, ny]
                        alpha = max(alpha, val[0])
                        cell[nx][ny] = 0
                        board_xor = board_xor ^ xor_val[nx][ny][1]
                        if beta <= alpha:
                            break
            xor_val_data[mask] = [C_val, move]
            return [C_val, move]
        else:
            move = []
            C_val = 1000000000000000
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if cell[i][j] == 0: continue
                    for dir in range(8):
                        nx = i + adjx[dir]
                        ny = j + adjy[dir]
                        if nx == 0 or nx == BOARD_SIZE or ny == 0 or ny == BOARD_SIZE or cell[nx][ny] != 0: continue
                        cell[nx][ny] = 2
                        board_xor = board_xor ^ xor_val[nx][ny][2]
                        val = self.minimax(_depth - 1, alpha, beta, True)
                        if C_val > val[0]:
                            C_val = val[0]
                            move = [nx, ny]
                        beta = min(beta, val[0])
                        cell[nx][ny] = 0
                        board_xor = board_xor ^ xor_val[nx][ny][2]
                        if beta <= alpha:
                            break
            xor_val_data[mask] = [C_val, move]
            return [C_val, move]

    def check_first_move(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if cell_val[i][j] != 0:
                    return False
        return True

    def make_move(self):
        if self.check_first_move():
            return [7, 7]
        else:
            return self.minimax(self.depth, -1000000000000000, 1000000000000000, True)[1]


ai = AI(1)

'''
GAME RUN
'''
while True:
    mouseX = -1
    mouseY = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if turn == 3 or turn == 4:
                with open("config.xor_value", "wb") as wf:
                    pickle.dump(xor_val_data, wf)
                    rf.close()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            break

    if turn == 0:
        cell = cell_val.copy()
        nmove = ai.make_move()
        cell_val[nmove[0]][nmove[1]] = 1
        board_xor = board_xor ^ xor_val[nmove[0]][nmove[1]][1]
        just_check = [nmove[0], nmove[1]]
        turn = (turn + 1) % 2
    elif turn == 1:
        mouse_Cell = []
        if mouseX != -1:
            mouse_Cell = [mouseX // cell_size, mouseY // cell_size]

        if check_Cell(mouse_Cell):
            turn = (turn + 1) % 2

    if Check_winner():
        turn = 3
    elif Check_draw():
        turn = 4

    draw_screen()