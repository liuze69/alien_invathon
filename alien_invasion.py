import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint
from star import Star
from time import sleep
from game_stats import GameStats
from button import Button
from score import Scoreboard

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.shoot_sound = pygame.mixer.Sound('sound/shoot.mp3')
        self.bg_image = pygame.image.load('images/OIP-C(1).jpg')
        self.alien = pygame.sprite.Group()
        
        # 背景音乐
        pygame.mixer.music.load('sound/坤坤开团神曲_爱给网_aigei_com.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.stars = pygame.sprite.Group()
        self._create_stars()
        
        self._create_fleet()

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.game_active = False  # 游戏是否处于活动状态
        #self.game_over = False  # 游戏是否结束
        self.play_button = Button(self, "Play") 
        self.font = pygame.font.SysFont(None, 48)

        



    def _create_fleet(self):
            alien = Alien(self)
            alien_width = alien.rect.width
            alien_height = alien.rect.height
            current_x,current_y = alien_width, alien_height
            while current_y < (self.settings.screen_height-2*alien_height):
                while current_x < (self.settings.screen_width -2*alien_width):
                    self._create_alien(current_x,current_y)
                    current_x += 2*alien_width
                current_y += 2*alien_height
                current_x = 2*alien_width



    def _create_alien(self,x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = new_alien.x
        new_alien.y = y_position
        new_alien.rect.y = new_alien.y
        self.alien.add(new_alien)
                
  

    def _check_events(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                #上下左右
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                 self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            self.game_active = True

            self.stats.reset_stats()
            self.scoreboard.prep_score()
            self.bullets.empty()
            self.alien.empty()

            self._create_fleet()
            self.ship.center_ship()



                
    
    def _check_keydown_events(self,event):
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = True
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet()
                elif event.key == pygame.K_p:
                    self._stop_game()
                elif event.key == pygame.K_q:
                     sys.exit()

    def _stop_game(self):
        self.game_active = False

    def _fire_bullet(self):
        if self.game_active:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)
                self.shoot_sound.play()

        

    def _check_keyup_events(self,event):
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                elif event.key == pygame.K_UP:
                    self.ship.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = False
    


    def _update_screen(self):
        self.screen.blit(self.bg_image, (0, 0))
        for star in self.stars.sprites():
            star.draw_star()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.alien.draw(self.screen)
        self.scoreboard.show_score()  # 显示得分
        if not self.game_active:
            self.play_button.draw_button()
        


    def _update_bullets(self, star_collided=False):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查子弹与星星的碰撞
        if not star_collided:
            collisions = pygame.sprite.groupcollide(self.bullets, self.alien, True, True)
            if collisions:
                self.stats.score += self.settings.alienpoints
                self.scoreboard.prep_score()
                self.scoreboard.check_high_score()  # 更新得分显示
        else:
            collisions = pygame.sprite.groupcollide(self.bullets, self.alien, False, True)
            if collisions:
                self.stats.score += self.settings.alienpoints
                self.scoreboard.prep_score()
                self.scoreboard.check_high_score()  # 更新得分显示

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.alien, True, True)
        if not self.alien:
            self.bullets.empty()
            self._create_fleet()
            
       
        


    def _check_fleet_edges(self):
        for alien in self.alien.sprites():
            if alien.check_edges():
                self._change_alien_direction()
                break



    def _change_fleet_direction(self):
        for alien in self.alien.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

        

    def _update_aliens(self):
        for alien in self.alien.sprites():
            if alien.check_edges():
                alien.rect.y += self.settings.fleet_drop_speed
                alien.direction *= -1
            alien.update()

        # 检查外星人是否撞到飞船或到达底部
        if pygame.sprite.spritecollideany(self.ship, self.alien):
            self._ship_hit()
        else:
            for alien in self.alien.sprites():
                if alien.rect.bottom >= self.screen.get_rect().bottom:
                    self._ship_hit()
                    break
        

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.alien.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False  # 游戏结束
            #self.ship.over_ship()
            self._show_game_over()
            sleep(3)
            self.scoreboard.zero_score() # 显示3秒Game Over
            
            self._reset_game()  # 重置游戏


    def _show_game_over(self):
        """显示Game Over文字"""
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect()
        text_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2)
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()



    def _reset_game(self):
        """重置游戏状态"""
        self.image = pygame.image.load('images/R-C.png')
        self.stats.reset_stats()
        self.bullets.empty()
        self.alien.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.game_active = True

        
    def _create_stars(self):
         for i in range(1): 
            x = randint(0, self.settings.screen_width - 50)
            y = randint(0, self.settings.screen_height - 50)
            star = Star(self, x, y)
            self.stars.add(star)
        


    def _update_stars(self):
         self.screen.blit(self.bg_image, (0, 0))
         for star in self.stars.sprites():
            star.draw_star()
         for bullet in self.bullets.sprites():
            bullet.draw_bullet()
         self.ship.blitme()
         self.alien.draw(self.screen)

        
    

    def run_game(self):
        star_collided = False  # 标记是否发生过star与飞船的碰撞
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_aliens()
            self._update_screen()
            pygame.display.flip()
            self.clock.tick(60)

            self._update_bullets(star_collided)
            

            # 检查star与飞船碰撞
            if not star_collided and pygame.sprite.spritecollideany(self.ship, self.stars):
                collided_star = pygame.sprite.spritecollideany(self.ship, self.stars)
                self.stars.remove(collided_star)
                star_collided = True
             



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()