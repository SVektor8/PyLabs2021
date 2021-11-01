import math
from random import choice
import pygame
from Colors import game_colors, white, red
from random import randint
from GraphComs import turn, distance


class Ball:
    def __init__(self, screen, radius):
        """
        Constructor of class Ball

            Args:
                screen: screen, where the ball will be drawn
                radius: radius of the ball
        """
        self.screen = screen
        self.r = radius
        self.color = 0x000000

        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0

    def move(self):
        """
        Moves the ball every single time interval

        Changes it's coordinates self.x and self.y and
        speed self.speed_x and self.speed_y due to speed and
        acceleration self.acceleration_x and self.acceleration_y
        """
        self.x += self.speed_x + self.acceleration_x / 2
        self.y += self.speed_y + self.acceleration_y / 2

        self.speed_x += self.acceleration_x
        self.speed_y += self.acceleration_y

    def draw(self):
        """
        Draws the ball on the screen self.screen
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def pos(self):
        """
        Returns position of the ball: a tuple of two numbers, it's x- and y- coordinates
        """
        return (self.x, self.y)

    def hit_test(self, ball):
        """
        Checks collision of the current Ball object with another ball

            Args:
                ball: object, with which collision is checked
            Returns:
                returns True if objects collided and False if they did not
        """
        if distance(self.pos(), ball.pos()) <= self.r + ball.r:
            return True
        else:
            return False


class Shell(Ball):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """
        Constructor of class Shell

            Args:
                screen: screen, where the shell will be drawn
                x: x-coordinate of the shell
                y: y-coordinate of the shell
        """
        super().__init__(screen, 10)
        self.x = x
        self.y = y

        self.color = choice(game_colors())  # color of the shell

        self.acceleration_y = 1  # gravitation


class Target(Ball):
    def __init__(self, screen):
        """
        Constructor of class Target

            Args:
                screen: screen, where the target will be drawn
        """
        super().__init__(screen, 26)

        self.points = 0  # summary points of the player
        self.color = red()

        self.new_target()

    def new_target(self):
        """
        Initialization of a new target
        """
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.r = randint(7, 50)

    def hit(self, points=1):
        """
        Shell terminates the target
        """
        self.points += points


class Gun:
    def __init__(self, screen, game):
        """
        Constructor of class Gun

            Args:
                screen: screen, where the ball will be drawn
                game: GameMaster object, where current game is launched
        """
        self.screen = screen
        self.f2_power = 10  # shot power
        self.f2_on = 0  # signal to a shot
        self.an = 1  # current angle between start speed of a shell and horizontal line
        self.x = 20
        self.y = 450
        self.game = game

    def fire2_start(self):
        """
        Aiming; from this point start speed of the shell is growing;
        happens if left mouse button is pushed
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """
        Shot by a shell; happens if left mouse button was released
        """
        self.game.bullet += 1

        new_ball = Shell(self.screen)  # shell is launched
        new_ball.r += 5

        # calculating angle
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))

        # calculating speed
        new_ball.speed_x = self.f2_power * math.cos(self.an)
        new_ball.speed_y = self.f2_power * math.sin(self.an)

        # adding to all balls and finishing shooting
        self.game.balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def aiming(self, event):
        """
        Aiming, depends on mouse position
        """
        if event:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))

    def draw(self):
        """
        Draws the gun
        """
        # calculating turned gun position
        coordinates = [turn(coo, self.an) for coo in [(-10, -3),
                                                      (self.f2_power, -3),
                                                      (self.f2_power, 3),
                                                      (-10, 3)]]
        coordinates = [(i[0] + 20, i[1] + 450) for i in coordinates]

        # drawing
        pygame.draw.polygon(self.screen,
                            (self.f2_power * 3 - 10, self.f2_power, self.f2_power),
                            coordinates)

    def power_up(self):
        """
        Making shot more powerful by lengthening the gun and making shells faster
        """
        if self.f2_on:
            if self.f2_power < 85:
                self.f2_power += 1


class GameMaster:
    def __init__(self, screen):
        """
        Constructor of class GameMaster

            Args:
                screen: screen, where all is happening
        """
        self.screen = screen

        # initialization of quantity of bullets(shells), balls, gun, target
        self.bullet = 0
        self.balls = []
        self.gun = Gun(screen, self)
        self.target = Target(screen)

        # finishing game marker
        self.finished = False

    def update(self):
        """
        Updates objects on the screen and draws them
        """
        # draws
        self.screen.fill(white())

        self.gun.draw()
        self.target.draw()
        for b in self.balls:
            b.draw()

        pygame.display.update()

        # moving, checking collisions, etc.
        for b in self.balls:
            b.move()
            if b.hit_test(self.target):
                self.target.hit()
                self.target.new_target()
        self.gun.power_up()

        # catching events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.gun.fire2_start()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                self.gun.aiming(event)
