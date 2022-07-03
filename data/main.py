import pygame, sys, time
from settings import *
from sprites import BG, Ground, Bird, Obstacle

class Game:

    
    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy-Bird')
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor 
        bg_height = pygame.image.load('../Flappy-Bird/graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites,self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.bird = Bird(self.all_sprites, self.scale_factor / 6)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # text
        self.font = pygame.font.Font('../Flappy-Bird/graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # menu
        # retry
        self.retry_surf = pygame.image.load('../Flappy-Bird/graphics/ui/retry.png').convert_alpha()
        self.retry_rect = self.retry_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # music
        self.music = pygame.mixer.Sound('../Flappy-Bird/sounds/sounds_music.wav')
        self.music.set_volume(0.1)
        self.music.play(loops = -1)

    def collisions(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, False, pygame.sprite.collide_mask)\
        or self.bird.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.bird.kill()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2  + (self.retry_rect.height / 1.5)

        score_surf = self.font.render(str(self.score), True, 'black' )
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.bird.jump()         
                    else:
                        self.bird = Bird(self.all_sprites, self.scale_factor / 6)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)
            
            # game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.collisions()
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active: 
                self.collisions()
            else:
                self.display_surface.blit(self.retry_surf, self.retry_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()