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

    def move_right(self):
        self.x += self.speed
        self.x = min(self.x,window.get_width()-self.image.get_width())
    def move_left(self):
        self.x -= self.speed
        self.x = max(0,self.x)
    def draw(self):
        window.blit(self.image, (self.x, self.y))


class Coin:
    def __init__(self,speed):
        self.speed = speed
        self.image = pygame.image.load("coin.png")
        self.set_random_coords()
    
    def move(self):
        self.x_y[1] += self.speed

    def set_random_coords(self):
        self.x_y=[random.randrange(0,window.get_width()-self.image.get_width()),-self.image.get_height()-random.randrange(0,window.get_height())]

    def draw(self):
        window.blit(self.image, (self.x_y[0], self.x_y[1]))


class CoinRain:
    def __init__(self, coin_speed, robot_speed, num_coins, points_to_win):
        pygame.init()

        self.robot=Robot(robot_speed)
        self.coins=[Coin(coin_speed) for n in range(num_coins)]

        self.num_coins = num_coins
        self.points_to_win = points_to_win

        pygame.display.set_caption('Rain of Coins')
        self.game_font = pygame.font.SysFont("Arial", 24)
        
        self.to_right = False
        self.to_left = False
        self.points = 0
        self.is_won = False
        self.is_lost = False

        self.clock = pygame.time.Clock()

        self.main_loop()

    def main_loop(self):
        def check_points():
            if self.points>=self.points_to_win:
                self.is_won=True

        while True:
            self.check_events()
            self.move_objects()
            check_points()
            self.draw()

            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False

            if event.type == pygame.QUIT:
                exit()

    def move_objects(self):
        self.move_robot()
        self.move_coins()
    
    def move_robot(self):
        if self.is_won or self.is_lost:
            return

        if self.to_right:
            self.robot.move_right()

        if self.to_left:
            self.robot.move_left()

    def move_coins(self):
        def is_under_robot(coin):
            return (self.robot.x>=coin.x_y[0] and self.robot.x<=coin.x_y[0]+coin.image.get_width()) or \
                (self.robot.x+self.robot.image.get_width()>=coin.x_y[0] and self.robot.x+self.robot.image.get_width()<=coin.x_y[0]+coin.image.get_width()) or \
                    (coin.x_y[0]>=self.robot.x and coin.x_y[0]<=self.robot.x+self.robot.image.get_width()) or \
                (coin.x_y[0]+coin.image.get_width()>=self.robot.x and coin.x_y[0]+coin.image.get_width()<=self.robot.x+self.robot.image.get_width())

        def is_nextto_robot(coin):
            return (coin.x_y[1]>=self.robot.y or coin.x_y[1]+coin.image.get_height()>=self.robot.y)

        def is_caughtby_robot(coin):
            return is_under_robot(coin) and is_nextto_robot(coin)

        if self.is_won or self.is_lost:
            return

        for n in range(self.num_coins):
            coin=self.coins[n]
            coin.move()
                
            if coin.x_y[1]>window_height:
                self.is_lost=True
            elif is_caughtby_robot(coin):
                self.points+=1
                coin.set_random_coords()

    def draw(self):
        def draw_end_message():
            won_message = self.game_font.render(f"You won!!!", True, (255, 0, 0))
            lost_message = self.game_font.render(f"You lost :(", True, (255, 0, 0))
            if self.is_won:
                window.blit(won_message, (window.get_width()/2-won_message.get_width()/2, window.get_height()/2-won_message.get_height()/2))
            elif self.is_lost:
                window.blit(lost_message, (window.get_width()/2-lost_message.get_width()/2, window.get_height()/2-lost_message.get_height()/2))

        def draw_counter():
            counter = self.game_font.render(f"Points: {self.points} ({self.points_to_win-self.points} to win)", True, (255, 0, 0))
            window.blit(counter, (window.get_width()-1.1*counter.get_width(), counter.get_height()))
        
        window.fill((0, 0, 0))

        self.robot.draw()
        for coin in self.coins:
            coin.draw()
        draw_counter()
        if self.is_won or self.is_lost:
            draw_end_message()

        pygame.display.flip()

if __name__ == "__main__":
    coin_speed=1
    robot_speed=2
    num_coins=2
    points_to_win=3
    CoinRain(coin_speed, robot_speed, num_coins, points_to_win)