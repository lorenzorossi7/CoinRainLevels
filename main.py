# Complete your game here
import pygame
import random

window_width=640
window_height=480
window = pygame.display.set_mode((window_width, window_height))

class Robot:
    def __init__(self,speed):
        self.speed = speed
        self.image = pygame.image.load("robot.png")
        self.x = window.get_width()/2-self.image.get_width()/2
        self.y = window.get_height()-self.image.get_height()
        self.to_right = False
        self.to_left = False

    def move(self):
        if self.to_right:
            self.x += self.speed
            self.x = min(self.x,window.get_width()-self.image.get_width())
        if self.to_left:
            self.x -= self.speed
            self.x = max(0,self.x)

    def draw(self):
        window.blit(self.image, (self.x, self.y))

class FallingObject:
    def __init__(self,speed,object_name):
        self.image = pygame.image.load(object_name)
        self.speed = speed
        self.set_random_coords()

    def set_random_coords(self):
        self.x_y=[random.randrange(0,window.get_width()-self.image.get_width()),-self.image.get_height()-random.randrange(0,window.get_height())]

    def move(self):
        self.x_y[1] += self.speed

    def draw(self):
        window.blit(self.image, (self.x_y[0], self.x_y[1]))

    def is_gone(self):
        return self.x_y[1]>window.get_height()

    def is_caught_by(self,robot: Robot):
        def is_above(robot: Robot):
            is_below_robot = self.x_y[1]>robot.y+robot.image.get_height()
            is_left_side_above_robot = self.x_y[0]>=robot.x and self.x_y[0]<=robot.x+robot.image.get_width()
            is_right_side_above_robot = self.x_y[0]+self.image.get_width()>=robot.x and self.x_y[0]+self.image.get_width()<=robot.x+robot.image.get_width()
            is_entirely_above_robot = self.x_y[0]<=robot.x and self.x_y[0]+self.image.get_width()>=robot.x+robot.image.get_width()
            is_above_robot = is_right_side_above_robot or is_left_side_above_robot or is_entirely_above_robot
            return (not is_below_robot) and is_above_robot
                
        def is_next_to(robot: Robot):
            return (self.x_y[1]>=robot.y or self.x_y[1]+self.image.get_height()>=robot.y)
    
        return is_above(robot) and is_next_to(robot)


class Coin(FallingObject):
    def __init__(self,speed):
        super().__init__(speed,"coin.png")

class Monster(FallingObject):
    def __init__(self,speed):
        super().__init__(speed,"monster.png")

class CoinRainLevel:
    def __init__(self, level):
        self.level=level
                 
        self.robot_speed, self.num_coins, self.coin_speed, self.num_monsters, self.monster_speed, self.points_to_win = self.get_difficulty(self.level)

        self.robot=Robot(self.robot_speed)
        self.coins=[Coin(self.coin_speed) for n in range(self.num_coins)]
        self.monsters=[Monster(self.monster_speed) for n in range(self.num_monsters)]

        self.game_font = pygame.font.SysFont("Arial", 24)
        self.points = 0
        self.is_won = False
        self.is_lost = False

    def get_difficulty(self,level):
        if level==0:
            robot_speed=2
            num_coins=2
            coin_speed=1
            num_monsters=0
            monster_speed=0
            points_to_win=2
        elif level==1:
            robot_speed=2
            num_coins=3
            coin_speed=1
            num_monsters=1
            monster_speed=1
            points_to_win=3
        elif level==2:
            robot_speed=2
            num_coins=3
            coin_speed=1
            num_monsters=2
            monster_speed=1
            points_to_win=4
        elif level==3:
            robot_speed=2
            num_coins=2
            coin_speed=1
            num_monsters=2
            monster_speed=2
            points_to_win=5
        elif level==4:
            robot_speed=2
            num_coins=2
            coin_speed=2
            num_monsters=2
            monster_speed=2
            points_to_win=3
        return robot_speed,num_coins,coin_speed,num_monsters,monster_speed,points_to_win

    def execute(self):
        def check_points():
            if self.points>=self.points_to_win:
                self.is_won=True

        self.check_events()
        self.move_objects()
        check_points()
        self.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.robot.to_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.robot.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.robot.to_right = False

            if event.type == pygame.QUIT:
                exit()

    def move_objects(self):
        self.move_robot()
        self.move_coins()
        self.move_monsters()
    
    def move_robot(self):
        if self.is_won or self.is_lost:
            return
        self.robot.move()

    def move_coins(self):
        if self.is_won or self.is_lost:
            return

        for n in range(self.num_coins):
            coin=self.coins[n]
            coin.move()
            if coin.is_gone():
                self.is_lost=True
            elif coin.is_caught_by(self.robot):
                self.points+=1
                coin.set_random_coords()

    def move_monsters(self):
        if self.is_won or self.is_lost:
            return

        for n in range(self.num_monsters):
            monster=self.monsters[n]
            monster.move()
            if monster.is_gone():
                monster.set_random_coords()
            if monster.is_caught_by(self.robot):
                self.points-=1
                monster.set_random_coords()

    def draw(self):
        def draw_counter():
            counter = self.game_font.render(f"Points: {self.points} ({self.points_to_win-self.points} to win)", True, (255, 0, 0))
            window.blit(counter, (window.get_width()-1.1*counter.get_width(), counter.get_height()))
        
        window.fill((0, 0, 255))
        pygame.display.set_caption(f'Rain of Coins - Level {self.level+1}')
        self.robot.draw()
        for coin in self.coins:
            coin.draw()
        for monster in self.monsters:
            monster.draw()
        draw_counter()
        pygame.display.flip()

class CoinRainGame:
    def __init__(self):
        pygame.init()
        self.num_levels = 5
        self.coinrain_levels =[CoinRainLevel(level) for level in range(self.num_levels)]

        self.game_font = self.coinrain_levels[0].game_font
        self.clock = pygame.time.Clock()
        self.is_won = False
        self.is_lost = False

    def execute(self):
        self.main_loop()
        self.final_page_loop()

    def main_loop(self):
        while True:
            for l in range(self.num_levels):
                coinrain_level=self.coinrain_levels[l]
                if not (coinrain_level.is_won or coinrain_level.is_lost):
                    coinrain_level.execute()
                    if coinrain_level.is_lost:
                        self.is_lost=True
                    if l==self.num_levels-1 and coinrain_level.is_won:
                        self.is_won=True
                    break
                    
            if self.is_won or self.is_lost:
                break
            self.clock.tick(60)

    def final_page_loop(self):
        while True:
            self.draw_final_page()
            self.check_final_page_events()
            self.clock.tick(60)

    def draw_final_page(self):
        window.fill((0, 0, 255))

        if self.is_won:
            won_message = self.game_font.render("You won!!!", True, (255, 0, 0))
            window.blit(won_message, (window.get_width()/2-won_message.get_width()/2, window.get_height()/2-won_message.get_height()/2))
        elif self.is_lost:
            lost_message = self.game_font.render("You lost :(", True, (255, 0, 0))
            window.blit(lost_message, (window.get_width()/2-lost_message.get_width()/2, window.get_height()/2-lost_message.get_height()/2))

        pygame.display.flip()

    def check_final_page_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == "__main__":
    CoinRainGame().execute()