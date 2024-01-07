import pygame
from sys import exit

width, height = 800, 600
pygame.init()
game_running = False
running = True
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('gra')
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 36)
original_bg = pygame.image.load('tlo.jpg')
bg = pygame.transform.scale(original_bg, (800, 600))
BORDER = pygame.Rect(width // 2 - 5, 0, 10, height)
player_bullets = []
enemy_bullets = []
bullet_vel = 7
max_bullets = 3
player_hit = pygame.USEREVENT + 1  # HP
enemy_hit = pygame.USEREVENT + 2  # HP
blue = (50, 50, 2)


class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Player:
    def __init__(self, x, y, width, height, speed, hp):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.hp = hp

    def move(self, keys):
        new_rect = self.rect.copy()
        if keys[pygame.K_a] and self.rect.x > 0:  
            new_rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < width - self.rect.width:  
            new_rect.x += self.speed
        if keys[pygame.K_w] and self.rect.y > 0:  
            new_rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < height - self.rect.height:  
            new_rect.y += self.speed

        # kolizja z borderem
        if not new_rect.colliderect(BORDER):
            self.rect = new_rect

        # kolizja z ekranem
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))


class Enemy:
    def __init__(self, x, y, width, height, speed, hp):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.hp = hp

    def move(self, keys):
        new_rect = self.rect.copy()
        if keys[pygame.K_LEFT] and self.rect.x > 0:  
            new_rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < width - self.rect.width:  
            new_rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:  
            new_rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < height - self.rect.height:  
            new_rect.y += self.speed

        # kolizja z borderem
        if not new_rect.colliderect(BORDER):
            self.rect = new_rect

        # kolizja z ekranem
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)


class Bullet:
    def __init__(self, x, y, direction_x, direction_y):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed_x = 10 * direction_x
        self.speed_y = 10 * direction_y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def off_screen(self):
        return self.rect.x > width or self.rect.x < 0 or self.rect.y > height or self.rect.y < 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)


class Button:
    def __init__(self, x, y, width, height, color, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


button_start = Button(150, 150, 200, 75, (0, 0, 255), "Start Game")
button_exit = Button(0, 0, 200, 50, (255, 0, 0), "Exit", action=lambda: set_game_running(False))

player = Player(0, height / 2, 50, 50, 5, 30)  #tutaj zmiana ilosci hp
enemy = Enemy(width - 50, height / 2, 50, 50, 5, 30)   


def set_game_running(value):
    global game_running
    game_running = value




def draw_button(button):
    pygame.draw.rect(screen, button.color, button.rect)
    text = font.render(button.text, True, (255, 255, 255))
    text_rect = text.get_rect(center=button.rect.center)
    screen.blit(text, text_rect)


def draw_window(border):
    pygame.draw.rect(screen, (0, 0, 0), border)


def handle_bullets(player_bullets, enemy_bullets, player, enemy):
    for bullet in player_bullets:
        bullet.move()
        bullet.draw(screen)
        if bullet.off_screen():
            player_bullets.remove(bullet)
        elif enemy.rect.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(enemy_hit))
            player_bullets.remove(bullet)
            enemy.hp -= 1  # odjecie hp przy kolizji
            if enemy.hp <= 0:
                show_winner("BLUE")
                reset_game()  # Dodaj to wywołanie przy wygranej
    for bullet in enemy_bullets:
        bullet.move()
        bullet.draw(screen)
        if bullet.off_screen():
            enemy_bullets.remove(bullet)
        elif player.rect.colliderect(bullet.rect):
            pygame.event.post(pygame.event.Event(player_hit))
            enemy_bullets.remove(bullet)
            player.hp -= 1  # odjecie hp przy kolizji
            if player.hp <= 0:
                show_winner("RED")
                reset_game()  # Dodaj to wywołanie przy wygranej


def show_winner(color):
    winner_text = font.render(f'{color} WINS!', True, (0, 0, 0))
    screen.blit(winner_text, (width // 2 - winner_text.get_width() // 2, height // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)  # opóznienie 2 sekundowe zanim tekst sie wyswietli


def reset_game():
    global game_running, player, enemy, bg
    game_running = False
    player.hp = 30
    enemy.hp = 30
    bg = pygame.transform.scale(original_bg, (800, 600))



while running:
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if button_start.is_clicked(pos):
                game_running = True
                bg.fill((255, 255, 255))
            elif button_exit.is_clicked(pos):
                if game_running:
                    reset_game()
                else:
                    running = False

    if game_running:
        draw_window(BORDER)
        keys = pygame.key.get_pressed()
        player.move(keys)
        enemy.move(keys)
        enemy.draw(screen)
        pygame.draw.rect(screen, (1, 163, 245), player.rect)
        if keys[pygame.K_ESCAPE]:
            reset_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(player_bullets) < max_bullets:
                bullet = Bullet(player.rect.x + player.rect.width, player.rect.y + player.rect.height // 2 - 2, 1, 0)
                player_bullets.append(bullet)
                print(bullet)
            if event.key == pygame.K_RCTRL and len(enemy_bullets) < max_bullets:
                bullet = Bullet(enemy.rect.x, enemy.rect.y + enemy.rect.height // 2 - 2, -1, 0)
                enemy_bullets.append(bullet)
        handle_bullets(player_bullets, enemy_bullets, player, enemy)

        # Draw HP
        player_hp_text = font.render(f'BLUE HP: {player.hp}', True, (0, 102, 239))
        screen.blit(player_hp_text, (10, 50))

        enemy_hp_text = font.render(f'RED HP: {enemy.hp}', True, (255, 0, 0))
        screen.blit(enemy_hp_text, (width - enemy_hp_text.get_width() - 10, 50))

    else:
        draw_button(button_start)

    draw_button(button_exit)
    pygame.display.update()
    clock.tick(60)
