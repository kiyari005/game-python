import sys
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

from random import randint, choice

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('underworld')
        self.clock = pygame.time.Clock()
        self.running = True
        self.max_enemies = 14  # Giới hạn số lượng quái vật
        self.enemy_count = 0    # Đếm số quái vật hiện có
        self.spawn_cooldown = 0  # Thời gian tạm dừng sinh quái vật
        self.spawn_delay = 1000  # 30 giây        
        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
                                      
        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 400
        
        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_position = []
        
        #audio
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.impact_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.music.play(loops = -1)
        
        #setup
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        
        folders = list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('images', 'enemies', folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
                
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:        
                self.can_shoot = True
            
    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():          
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)     
            
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))    
            
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
            
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_position.append((obj.x, obj.y))
                
    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact_sound.play
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()
                
    def player_collision(self):
     if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
        self.player.take_damage(10)  # Giảm 10 máu khi va chạm với quái vật

    def draw_lives(self):
     font = pygame.font.Font(None, 36)
     lives_text = font.render(f'Lives: {self.player.lives}', True, (255, 255, 255))
     self.display_surface.blit(lives_text, (10, 40))  # Vẽ số mạng ở vị trí (10, 40)
 
    def draw_health_bar(self):
    # Kích thước và vị trí thanh máu
     health_bar_rect = pygame.Rect(10, 10, 200, 25)
     current_health_rect = pygame.Rect(10, 10, 200 * (self.player.health / self.player.max_health), 25)
    
    # Vẽ thanh máu
     pygame.draw.rect(self.display_surface, (255, 0, 0), health_bar_rect)  # Màu nền đỏ
     pygame.draw.rect(self.display_surface, (0, 255, 0), current_health_rect)  # Màu máu xanh lá

    def run(self):
     while self.running:
        # dt
        dt = self.clock.tick() / 1000
    
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == self.enemy_event:
                Enemy(choice(self.spawn_position), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

        # update
        self.gun_timer()
        self.input()
        self.all_sprites.update(dt)
        self.bullet_collision()
        self.player_collision()
    
        # draw
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.rect.center)
        self.draw_health_bar()  # Vẽ thanh máu
        self.draw_lives()        # Vẽ số mạng
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':        
    game = Game()
    game.run()
