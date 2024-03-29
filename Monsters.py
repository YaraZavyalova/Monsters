import os
import sys
import random

import sqlite3
import pygame

pygame.init()
size = WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50
gravity = 0.25
columns = 4
rows = 1
screen_rect = (0, 0, WIDTH, HEIGHT)
camera_move = True
coin_num = 0
map_num = 1
death = False
game_win = False


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Цель игры:",
                  "Собирите все монеты, ",
                  "преодолеть препятствия и добраться до финиша живым."
                  "Персонажем можно управлять с помощью стрелочек(или WASD).",
                  "Чтобы начать уровень заново нажмите 'r'.",
                  "Удачи!"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def victory_screen():
    global map_num
    global game_win
    if map_num < 3:
        intro_text = ["Вы Выграли!", "",
                      "Нажмите на экран чтобы продолжить на",
                      "следующий уровень.", "Можно сохранить свой прогресс в игре при помощи клавиш цифр"]

        fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        game_win = True
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)


def death_screen():
    global camera_move
    global death
    intro_text = [" Вы проиграли!", "",
                  "Цель игры:",
                  "Собирите все монеты, ",
                  "преодолеть препятствия и добраться до финиша живым."
                  "Персонажем можно управлять с помощью стрелочек(или WASD)."
                  "Чтобы начать уровень заново нажмите 'r'."]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 100)
    text_coord = 250
    camera_move = False
    death = True
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        main()
        clock.tick(FPS)


def savefile_screen():
    global map_num
    global WIDTH
    intro_text = ["Вы хотите сохранить свой прогресс?", "",
                  "Нажмите S если хотите сохранить",
                  "Нажмите O если хотите открыть уже сохранёный прогресс"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return 'S'
                if event.key == pygame.K_o:
                    return 'O'
        pygame.display.flip()
        clock.tick(FPS)


def save_over_file_screen():
    global map_num
    global WIDTH
    intro_text = ["Вы хотите сохранить свой прогресс? Тут уже есть сохранёный прогресс", "",
                  "Нажмите Y если хотите сохранить",
                  "Нажмите N если нет"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return 'Y'
                if event.key == pygame.K_n:
                    return 'N'
        pygame.display.flip()
        clock.tick(FPS)


def no_save_screen():
    global map_num
    global WIDTH
    intro_text = ["Нет такого файла", "", ]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()


def generate_level(level):
    global coin_num
    new_player, x, y, new_monster, exit_door = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                coin_num += 1
                Tile('empty', x, y)
                Coin(x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                new_monster = Monster(x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                exit_door = Exit(x, y)
            elif level[y][x] == '^':
                Tile('empty', x, y)
                Spike(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, new_monster, exit_door


tile_images = {
    'wall': load_image('bricks.png'),
    'empty': load_image('Empty.png')
}
coin_image = load_image('coin.png')
spike_image = load_image('Spike.png')
player_image = load_image('Player\Idle\Player_Idle_frame1.png'), load_image('Player\Idle\Player_Idle_frame2.png')
monster_image = load_image('Monster\Monster_Idle_frame1.png'), load_image('Monster\Monster_Idle_frame2.png')
exit_image = load_image('Gate\Gate_Closed.png'), load_image('Gate\Gate_Opened.png')
player_walk_sheet = load_image('Player_Walk.png'), load_image('Player_Walk_Left.png')
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.tile_type = tile_type
        if tile_type == 'wall':
            self.mask = pygame.mask.from_surface(self.image)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("Blood.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity

    def update(self, *args):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class MoneyRain(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("Coin.png")]
    for scale in (10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость - это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой
        self.gravity = gravity

    def update(self, *args):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles_money(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        MoneyRain(position, random.choice(numbers), random.choice(numbers))


MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 100)


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group, all_sprites)
        self.image = exit_image[0]
        self.exit_open = False
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def open(self, sprite):
        global coin_num
        if coin_num == 0:
            self.image = exit_image[1]
            self.exit_open = True
        if pygame.sprite.collide_mask(self, sprite) and self.exit_open:
            victory_screen()
            if map_num == 3:
                create_particles_money((sprite.rect.x, sprite.rect.y))


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monster_group, all_sprites)
        self.frame = 0
        self.image = monster_image[0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if args[0].type == MYEVENTTYPE:
            if self.frame == 1:
                self.image = monster_image[0]
                self.frame = 0
            else:
                self.image = monster_image[1]
                self.frame = 1

    def collide_with(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            create_particles((sprite.rect.x, sprite.rect.y))
            sprite.killed()


class Spike(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(spike_group, all_sprites)
        self.image = spike_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def collide_with(self, sprite):
        if pygame.sprite.collide_mask(self, sprite):
            create_particles((sprite.rect.x, sprite.rect.y))
            sprite.killed()


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coin_group, all_sprites)
        self.image = coin_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def collect(self, sprite):
        global coin_num
        if self.rect.colliderect(sprite.rect):
            self.image = tile_images['empty']
            coin_num -= 1
            self.kill()


class Player(pygame.sprite.Sprite):
    jump = False
    move_left = False
    move_right = False

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.x_start = pos_x
        self.y_start = pos_y
        self.frames = []
        self.animations = []
        self.cut_sheet(player_walk_sheet[0], columns, rows)
        self.cut_sheet(player_walk_sheet[1], columns, rows)
        self.cur_frame = 0
        self.image = player_image[0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)
        self.frame = 0
        self.gravity = gravity
        self.velocity = [self.rect.x, self.rect.y]
        self.dx = 0
        self.dy = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        self.animations.append(self.frames)
        self.frames = []

    def move(self, dx, dy):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self, *args):
        for elem in tiles_group:
            if pygame.sprite.collide_mask(self, elem):
                if self.rect.y > 0:
                    self.rect.bottom = elem.rect.top
                elif self.rect.y < 0:
                    self.rect.top = elem.rect.bottom
        if args[0].type == MYEVENTTYPE:
            if self.move_right:
                self.cur_frame = (self.cur_frame + 1) % len(self.animations[0])
                self.image = self.animations[0][self.cur_frame]
            if self.move_left:
                self.cur_frame = (self.cur_frame + 1) % len(self.animations[1])
                self.image = self.animations[1][self.cur_frame]

    def killed(self):
        self.rect.move(self.x_start, self.y_start)
        self.kill()
        death_screen()
        self.rect.y = self.y_start
        self.rect.x = self.x_start


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        if camera_move:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        if camera_move:
            self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
            self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def main():
    global map_num
    global camera_move
    global death
    global game_win
    global coin_num
    player, level_x, level_y, monster, exit_door = generate_level(load_level(f'levels/level_{map_num}.txt'))
    camera_move = True
    start_screen()
    step = 15
    jump_height = 12
    y_gravity = 1
    y_vel = jump_height
    camera = Camera()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.rect.y += 5
            all_sprites.update(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.jump = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move_right = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move_left = True
                if event.key == pygame.K_r:
                    death = True
                if event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2:
                    answer = savefile_screen()
                    con = sqlite3.connect('data/saves.sqlite')
                    cur = con.cursor()
                    result = cur.execute("""SELECT savefiles FROM Saves""").fetchall()
                    saves = []
                    keys = {pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4,
                            pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9}
                    for name in result:
                        saves.append(name[0])
                    if answer == 'S':
                        if keys[event.key] in saves:
                            yes_no = save_over_file_screen()
                            if yes_no == 'N':
                                break
                            if yes_no == 'Y':
                                cur.execute(f"""UPDATE Saves
                                SET levels = '{map_num}' WHERE savefiles = '{keys[event.key]}'""")
                        else:
                            cur.execute(
                                f"""INSERT INTO Saves(savefiles,levels) VALUES('{keys[event.key]}','{map_num}')""")
                    elif answer == 'O':
                        if keys[event.key] in saves:
                            map_num = cur.execute(f"""SELECT levels FROM Saves
                                WHERE savefiles = '{keys[event.key]}'""").fetchall()[0][0]
                            death = True

                        else:
                            no_save_screen()
                    con.commit()
                    con.close()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move_right = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move_left = False
            if player.jump:
                player.rect.y -= y_vel
                y_vel -= y_gravity
                if y_vel < - jump_height:
                    player.jump = False
                    y_vel = jump_height
                player.rect.y -= y_vel
            if player.move_right:
                player.rect.x += step
            if player.move_left:
                player.rect.x -= step
            player.rect.move(0, 1)
        fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        for coin in coin_group:
            coin.collect(player)
        for spike in spike_group:
            spike.collide_with(player)
        for monster in monster_group:
            monster.collide_with(player)
        if death or game_win:
            for elem in all_sprites:
                elem.kill()
            coin_num = 0
            if death:
                death = False
                player, level_x, level_y, monster, exit_door = generate_level(load_level(f'levels/level_{map_num}.txt'))
            if game_win:
                game_win = False
                if map_num < 3:
                    map_num += 1
                    player, level_x, level_y, monster, exit_door = generate_level(
                        load_level(f'levels/level_{map_num}.txt'))
        exit_door.open(player)
        coin_group.draw(screen)
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        player_group.draw(screen)
        dark = pygame.transform.scale(load_image('Darkness.png'), (WIDTH, HEIGHT))
        screen.blit(dark, (0, 0))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
