import pygame,sys
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('.\\graphics\\player\\up\\up_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-5,0)

        self.import_player_assets()
        self.status = 'down'

        #self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attcak_time = None

        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        print(self.weapon)
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.stats = {'health': 100,'energy':60,'attack': 10,'magic': 4,'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        self.vulnarable = True
        self.hurt_time = None
        self.invulnarability_duration = 500

    def import_player_assets(self):
        character_path = '.\\graphics\\player\\'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 
                        'right_idle':[], 'left_idle':[], 'up_idle':[], 'down_idle':[],
                        'right_attack':[], 'left_attack':[], 'up_attack':[], 'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            #movement
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            #attack
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            #magic
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]
            
            #if keys[pygame.K_e] and self.can_switch_weapon:
             #   self.can_switch_weapon = False
              #  self.weapon_switch_time = pygame.time.get_ticks()

               # if self.weapon_index == 1:
               #     self.weapon_index = 0
                #else:
                #    self.weapon = 1

                #self.weapon = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):

        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

            if not self.can_switch_weapon:
                if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                    self.can_switch_weapon = True

        if not self.vulnarable:
            if current_time - self.hurt_time >= self.invulnarability_duration:
                self.vulnarable = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnarable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def check_death(self):
        if self.health <=0:
            pygame.quit()
            sys.exit()

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def update(self):
        self.check_death()
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)