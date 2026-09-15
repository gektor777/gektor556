import random
import sys
import pygame


class Block:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self, surf):
        pygame.draw.rect(surf, (200, 30, 30), self.rect)


class Player:
    def __init__(self, x, y, w=50, h=15, speed=6):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed

    def move(self, dx, bounds):
        self.rect.x += dx * self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > bounds[0]:
            self.rect.right = bounds[0]

    def draw(self, surf):
        pygame.draw.rect(surf, (50, 150, 250), self.rect)


class Game:
    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Dodge the Blocks")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.reset()

    def reset(self):
        self.player = Player(self.width // 2 - 25, self.height - 40)
        self.blocks = []
        self.spawn_timer = 0
        self.spawn_interval = 700  # milliseconds
        self.running = True
        self.score = 0
        self.game_over = False

    def spawn_block(self):
        w = random.randint(20, 80)
        x = random.randint(0, self.width - w)
        speed = random.uniform(2.0, 5.0)
        b = Block(x, -20, w, 20, speed)
        self.blocks.append(b)

    def handle_events(self):
        dx = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_r:
                    self.reset()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        self.player.move(dx, (self.width, self.height))

    def update(self, dt):
        if self.game_over:
            return

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawn_block()

        for b in list(self.blocks):
            b.update()
            if b.rect.top > self.height:
                self.blocks.remove(b)
                self.score += 1
            if b.rect.colliderect(self.player.rect):
                self.game_over = True

    def draw(self):
        self.screen.fill((30, 30, 30))
        for b in self.blocks:
            b.draw(self.screen)
        self.player.draw(self.screen)

        score_surf = self.font.render(f"Score: {self.score}", True, (240, 240, 240))
        self.screen.blit(score_surf, (10, 10))

        if self.game_over:
            go_surf = self.font.render("Game Over - Press R to restart", True, (255, 220, 50))
            rect = go_surf.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(go_surf, rect)

        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(60)
            self.handle_events()
            self.update(dt)
            self.draw()
