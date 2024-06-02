import pygame
from sqlite3 import connect as db_connect
from random import randint
from resources.functions import rand, get_resolution, one_return, dict_key_default, hd_textures as texture_type, full_screen
from resources.db import RecordField

pygame.init()

win = pygame.display.set_mode()
hearts = 3
clock = pygame.time.Clock()
is_game = True
is_win = False
temp_heart = True
texture_paths = texture_type('hd')
heart_texture = pygame.image.load('files/textures/heart/heart64.png').convert_alpha()
hearts_font = pygame.font.Font('files/fonts/PixBob-Lite-Free.ttf', 72)
text_font = pygame.font.Font('files/fonts/PTSans-Bold.ttf', 26)
wood_block = pygame.image.load(texture_paths.wood_block).convert_alpha()
gold_block = pygame.image.load(texture_paths.gold_block).convert_alpha()
blue_block = pygame.image.load(texture_paths.blue_block).convert_alpha()
bg_sound = pygame.mixer.Sound('files/sounds/bg_sound.mp3')
win_sound = pygame.mixer.Sound('files/sounds/win.wav')
bg_sound.play(-1)
background = pygame.transform.scale(pygame.image.load(texture_paths.background).convert_alpha(), get_resolution())
game_over = full_screen(texture_paths.game_over).convert_alpha()
win_screen = full_screen(texture_paths.win).convert_alpha()


def hearts_draw():
    global hearts, heart_texture, win, hearts_font
    if hearts >= 10:
        win.blit(heart_texture, (10, 10))
        hearts_count = hearts_font.render(str(hearts), True, 'red')
        y = 12
        win.blit(hearts_count, (80, y))
    else:
        x, y = 10, -60
        for i in range(hearts):
            if i != 1 and i % 3 == 0:
                y += 70
                x = 10
            win.blit(heart_texture, (x, y))
            x += 70


def blocks_init(width: int = 100, height: int = 20, **kwargs):
    global blocks, W, H
    sh_coff = dict_key_default(kwargs, 'sh_coff', 0.5)
    screen_height = int(round(H * sh_coff, 0))
    number_rows = W // width
    number_columns = screen_height // height
    number_blocks = number_rows * number_columns
    marginW = (W % width) // 2
    x, y = marginW, 0

    for i in range(number_blocks):
        if x + marginW == W:
            y += height
            x = marginW
        blocks.append(Block(x, y, width, height, randint(1, 3)))
        x += width


def blocks_render():
    global blocks
    for block in blocks:
        block.render()


def blocks_event_check():
    global blocks
    for block in blocks:
        block.event_check()


def all_blocks_destroyed(blocks_list: list) -> bool:
    dlist = list()
    output = True
    for block in blocks_list:
        dlist.append(block.isDestroyed())
    for block in dlist:
        if not block:
            output = False
            break
    return output


def plus_heart():
    global hearts
    hearts += 1


def new_record(name):
    global ticks, hearts
    connect = db_connect('db.db')
    cursor = connect.cursor()
    query = '''
    INSERT INTO records (name, time, hearts) VALUES
    ('{}', {}, {})
    '''
    cursor.execute(query.format(name, ticks, hearts))
    connect.commit()
    connect.close()


def game_over_win():
    global hearts, ticks, is_win
    window = RecordField(ticks, hearts, new_record)
    if is_win:
        window.mainloop()
    pygame.quit()
    exit()


W, H = get_resolution()
block_width, block_height = 200, 40
blocks = list()


class Board:
    def __init__(self, color='#736900', width: int = 200, speed: int = 10) -> None:
        self.color = color
        self.width = width
        self.x = (W - self.width) // 2
        self.y = H - 175
        self.speed = speed

    def draw(self):
        self.board = pygame.draw.rect(win, self.color, (self.x, self.y, self.width, 30))

    def actions_by_keys(self):
        global temp_heart, W
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            if self.x < W - self.width:
                self.x += self.speed
        elif keys[pygame.K_SPACE]:
            temp_heart = False


class Ball:
    def __init__(self, color='#4287f5', radius: int = 20):
        global board
        self.default_color, self.color = one_return(2, color)
        self.radius = radius
        self.dir_x, self.dir_y = rand(), 1
        self.x = 500
        self.y = board.y - self.radius
        self.spx, self.spy = 5, 5
        self.damage = 1

    def begin(self, board: Board):
        if temp_heart:
            self.x = board.x + board.width // 2
        else:
            self.x += self.dir_x * self.spx
            self.y -= self.dir_y * self.spy

            if self.x < 0 or self.x > W:
                self.dir_x = -self.dir_x

            if self.y < 0:
                self.dir_y = -self.dir_y
            elif self.y > H:
                self.dead()

            if self.ball.colliderect(board.board):
                self.dir_y = -self.dir_y
                self.y -= 20

            keys = pygame.key.get_pressed()

    def draw(self):
        self.ball = pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def dead(self):
        global hearts, temp_heart, is_game, is_win
        hearts -= 1
        if hearts == 0:
            is_game, is_win = one_return(2, False)
        else:
            temp_heart = True
            self.y = board.y - self.radius

    def rebound(self):
        self.dir_y = -self.dir_y


class Block(pygame.Rect):
    def __init__(self, x: int, y: int, width: int, height: int, strength: int):
        self.x, self.y, self.width, self.height, self.health = x, y, width, height, strength
        super().__init__(self.x, self.y, self.width, self.height)
        if strength == 1:
            self.texture = pygame.transform.scale(wood_block, (self.width, self.height))
        elif strength == 2:
            self.texture = pygame.transform.scale(gold_block, (self.width, self.height))
        elif strength == 3:
            self.texture = pygame.transform.scale(blue_block, (self.width, self.height))
        else:
            raise ValueError

    def render(self):
        if self.health > 0:
            win.blit(self.texture, self)

    def event_check(self):
        global ball, hearts

        if self.colliderect(ball.ball) and self.health > 0:
            self.health -= ball.damage
            ball.rebound()
            if self.isDestroyed():
                # Шанс 10%
                num = randint(1, 10)
                if num == 1:
                    hearts += 1

    def destroy(self):
        self.health = 0

    def isDestroyed(self) -> bool:
        return self.health == 0


board = Board()
ball = Ball()
blocks_init(block_width, block_height)
running = True

while running:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
    if is_game:
        win.blit(background, (0, 0))
        blocks_render()
        hearts_draw()
        board.draw()
        ball.draw()
        blocks_event_check()
        board.actions_by_keys()
        ball.begin(board)
        ticks = pygame.time.get_ticks()
        if all_blocks_destroyed(blocks):
            is_game, is_win = False, True
    else:
        over_color, over_aa = 'red', True

        bg_sound.stop()

        if is_win:
            win.blit(win_screen, (0, 0))
            ec = 578
        else:
            win.blit(game_over, (0, 0))
            ec = 756

        if is_win:
            pygame.display.update()
            win_sound.play()
            game_over_win()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit(ec)

    pygame.display.update()
    clock.tick(45)
