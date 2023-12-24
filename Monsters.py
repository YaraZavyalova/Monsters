import os
import sys

import pygame

pygame.init()
size = WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode(size)

all_sprites = pygame.sprite.Group()


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


class Player(pygame.sprite.Sprite):
    pass


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        dark = pygame.transform.scale(load_image('Darkness.png'), (WIDTH, HEIGHT))
        screen.blit(dark, (0, 0))
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
