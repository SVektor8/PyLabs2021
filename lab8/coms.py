import math
import datetime
import pygame
from random import choice, randrange
from Colors import game_colors, white, red, black, DARKKHAKI
from Colors import BERLIN_LAZUR, OLIVE, SKYBLUE, GRAY, WHITE
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
        self.max_speed = 1000

    def move(self):
        """
        Moves the ball every single time interval

        Changes it's coordinates self.x and self.y and
        speed self.speed_x and self.speed_y due to speed and
        acceleration self.acceleration_x and self.acceleration_y
        """

        self.x += self.speed_x + self.acceleration_x / 2
        self.y += self.speed_y + self.acceleration_y / 2

        if ((self.speed_x + self.acceleration_x) ** 2
            + (self.speed_y + self.acceleration_y) ** 2) ** 0.5 \
                <= self.max_speed:
            self.speed_x += self.acceleration_x
            self.speed_y += self.acceleration_y
        else:
            k = self.max_speed / (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5
            self.speed_x *= k
            self.speed_y *= k

    def draw(self):
        """
        Draws the ball on the screen self.screen like a circle
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
    def __init__(self, screen, game):
        """
        Constructor of class Target

            Args:
                screen: screen, where the target will be drawn
                game: GameMaster object, where current game is launched
        """
        super().__init__(screen, 26)

        self.points = 0  # summary points of the player
        self.color = red()
        self.game = game

        self.new_target()  # initialization of start target

    def new_target(self):
        """
        Initialization of a new target
        """
        self.x = randint(400, 780)
        self.y = randint(200, 550)
        self.r = randint(7, 40)

    def hit(self, points=1):
        """
        Shell terminates the target
        """
        self.game.points += points  # updating points

        self.game.level += points / self.game.level  # updating level

        if self.game.level >= 3:
            self.game.level += 0.15


class MovingTarget(Target):
    def __init__(self, screen, game):
        """
        Constructor of class Target

            Args:
                screen: screen, where the target will be drawn
                game: GameMaster object, where current game is launched
        """
        super().__init__(screen, game)
        self.speed_x = randrange(5, 10)
        self.speed_y = randrange(5, 10)

    def new_target(self):
        """
        Initialization of a new target
        """
        super().new_target()

        self.speed_x = randrange(1, 10)
        self.speed_y = randrange(1, 10)

    def move(self):
        """
        Moving the target; if it it touches the window border, it will go back
        """
        super().move()
        if not 0 < self.x < 800:
            self.speed_x *= -1
        if not 0 < self.y < 600:
            self.speed_y *= -1


class Gun(Ball):
    def __init__(self, screen, game):
        """
        Constructor of class Gun

            Args:
                screen: screen, where the ball will be drawn
                game: GameMaster object, where current game is launched
        """
        super().__init__(screen, -1)
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

        new_ball = Shell(self.screen, x=self.x, y=self.y)  # shell is launched
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
        self.new_ball = new_ball

    def aiming(self, event):
        """
        Aiming, depends on mouse position
        """
        if event:
            self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))

    def draw(self):
        """
        Draws the gun
        """
        # calculating turned gun position
        coordinates = [turn(coo, self.an) for coo in [(-10, -3),
                                                      (self.f2_power, -3),
                                                      (self.f2_power, 3),
                                                      (-10, 3)]]
        coordinates = [(i[0] + self.x, i[1] + self.y) for i in coordinates]

        # drawing
        pygame.draw.polygon(self.screen,
                            (self.f2_power * 3, self.f2_power, self.f2_power),
                            coordinates)

    def power_up(self):
        """
        Making shot more powerful by lengthening the gun and making shells faster
        """
        if self.f2_on:
            if self.f2_power < 42:
                self.f2_power += 1

    def move(self):
        """
        Moves the gun; it can't go outside of the screen
        """

        super().move()

        self.x %= 800


class Tank(Gun):
    """Child gun class; is drawn like a tank, has faster shells of less caliber"""

    def __init__(self, screen, game):
        """
        Constructor of class Gun
            Args:
                screen: screen, where the ball will be drawn
                game: GameMaster object, where current game is launched
        """
        super().__init__(screen, game)

        # defining start tank parameters
        self.x = 100
        self.y = 450
        self.max_speed = 10

    def draw(self):
        """
        Drawing the object like a tank not like usual gun
        """
        # gun
        coordinates = [turn(coo, self.an) for coo in [(-10, -1.5),
                                                      (self.f2_power + 36, -1.5),
                                                      (self.f2_power + 36, 1.5),
                                                      (-10, 1.5)]]
        coordinates = [(i[0] + self.x, i[1] + self.y) for i in coordinates]

        pygame.draw.polygon(self.screen,
                            (self.f2_power * 3, self.f2_power, self.f2_power),
                            coordinates)

        # turret
        coordinates = [turn(coo, 0) for coo in [(-42, 8),
                                                (0, 8),
                                                (-4, -6),
                                                (-35, -8),
                                                (-38, -1)]]
        coordinates = [(i[0] + self.x, i[1] + self.y) for i in coordinates]

        pygame.draw.polygon(self.screen,
                            DARKKHAKI(),
                            coordinates)

        # body
        coordinates = [turn(coo, 0) for coo in [(-80, 8),
                                                (30, 8),
                                                (43, 18),
                                                (27, 30),
                                                (-70, 30)]]
        coordinates = [(i[0] + self.x, i[1] + self.y) for i in coordinates]

        pygame.draw.polygon(self.screen,
                            DARKKHAKI(),
                            coordinates)

    def aiming(self, event):
        """
        Aiming, depends on mouse position
        """
        angle = math.pi / 4.5
        if event:
            try:
                angle = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
            except:
                self.an = math.pi / 4.5
            finally:
                if abs(angle) < math.pi / 4.5:
                    self.an = angle
                else:
                    self.an = math.pi / 4.5 * angle / abs(angle)

    def fire2_end(self, event):
        """
        Correcting parameters of new shell due to tank features
        """
        super().fire2_end(event)
        self.new_ball.r = 3
        self.new_ball.color = OLIVE()
        self.new_ball.speed_x *= 2.5
        self.new_ball.speed_y *= 2.5


class Plane(Gun):
    """Child gun class; is drawn like a plane, has smth like bombs with the same
    start speed as a plane itself"""

    def __init__(self, screen, game):
        """
        Constructor of class Gun
            Args:
                screen: screen, where the ball will be drawn
                game: GameMaster object, where current game is launched
        """
        super().__init__(screen, game)

        # Defining plane's parameters
        self.x = 100
        self.y = 250
        self.speed_x = 8
        self.speed_y = -14
        self.max_speed = 50
        self.acceleration_y = 1

    def draw(self):
        """
        Drawing the object like a plane not like usual gun
        """

        coordinates = [(-60, -15, 120, 25)]  # body
        coordinates = [(i[0] + self.x, i[1] + self.y, i[2], i[3]) for i in coordinates]

        pygame.draw.ellipse(self.screen, black(), coordinates[0])

        coordinates = [(-48, -40, 20, 47)]  # rear of the plane
        coordinates = [(i[0] + self.x, i[1] + self.y, i[2], i[3]) for i in coordinates]

        pygame.draw.ellipse(self.screen, black(), coordinates[0])

        coordinates = [(55, -7)]  # window
        coordinates = [(i[0] + self.x, i[1] + self.y) for i in coordinates]

        pygame.draw.circle(self.screen, SKYBLUE(), coordinates[0], 5)

    def aiming(self, event):
        """
        Aiming, depends on mouse position
        """
        angle = math.pi / 4.5
        if event:
            try:
                angle = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
            except:
                self.an = math.pi / 4.5
            finally:
                if abs(angle) < math.pi / 4.5 and 0:
                    self.an = angle
                else:
                    self.an = math.pi / 4.5 * angle / abs(angle)

    def fire2_end(self, event):
        """
        Correcting parameters of new shell due to tank features
        """
        super().fire2_end(event)
        self.new_ball.r = 12
        self.new_ball.color = black()
        self.new_ball.speed_x = self.speed_x
        self.new_ball.speed_y = self.speed_y
        self.new_ball.acceleration_y = 1

    def move(self):
        """
        Moves the plane due to it's features: it can both fly and fall to the ground
        """
        super().move()
        if self.y >= 450:
            self.speed_x = 0
            self.speed_y = 0
            self.y = 450
        else:
            self.speed_x = 8


class GameMaster:
    highscore = -1
    username = 'admin'
    logged = False
    database_path = 'database.txt'
    data_path = 'data.txt'

    def __init__(self, screen):
        """
        Constructor of class GameMaster

            Args:
                screen: screen, where all is happening
        """
        self.screen = screen

        # initialization of quantity of bullets(shells), balls, gun, target
        self.bullet = 0
        self.points = 0
        self.balls = []
        self.armor = Gun(screen, self)
        self.targets = [Target(screen, self), MovingTarget(screen, self)]
        self.level = 1

        self.logger = EventLogger()
        self.login()

        # finishing game marker
        self.finished = False

    def update(self):
        """
        Updates objects on the screen and draws them
        """
        self.draw()
        self.write_stats()

        if 3 <= self.level < 5 and type(self.armor) != Tank:
            self.armor = Tank(self.screen, self)
        elif 5 <= self.level < 7 and type(self.armor) != Plane:
            self.armor = Plane(self.screen, self)

        # moving, checking collisions, etc.
        for b in self.balls:

            b.move()
            for target in self.targets:
                if b.hit_test(target):
                    target.hit()
                    target.new_target()
        self.armor.power_up()
        self.armor.move()

        for i in self.targets:
            i.move()

        # catching events
        self.events()

    def events(self):
        """
        Checks events and changes objects' acceleration etc.
        """
        for event in pygame.event.get():
            self.logger.get_event(event)

            if self.logged:
                if event.type == pygame.QUIT:
                    self.finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.armor.fire2_start()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.armor.fire2_end(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.armor.aiming(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if type(self.armor) == Tank:
                            self.armor.acceleration_x = -0.3

                    elif event.key == pygame.K_RIGHT:
                        if type(self.armor) == Tank:
                            self.armor.acceleration_x = 0.5
                    elif event.key == pygame.K_UP:
                        if type(self.armor) == Plane:
                            self.armor.acceleration_y -= 2.3
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        if type(self.armor) in [Tank]:
                            self.armor.acceleration_xx = 0
                    elif event.key == pygame.K_RIGHT:
                        if type(self.armor) in [Tank]:
                            self.armor.acceleration_x = 0
                    elif event.key == pygame.K_UP:
                        if type(self.armor) == Plane:
                            self.armor.acceleration_y += 2.3
            else:  # mode of changing the username
                if event.type == pygame.QUIT:
                    exit()  # Quits
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:  # deletes last symbol
                        self.username = self.username[:-1]
                    elif event.key == 13:  # Enter button, to go to game mode
                        self.logged = True
                        self.logger.write_event('User logged as ' + self.username)

                    elif 97 <= event.key <= 122:  # typing a letter
                        letters = 'abcdefghijklmnopqrstuvwxyz'
                        self.username += letters[event.key - 97]
                    elif 48 <= event.key <= 57:  # typing a digit
                        self.username += str(event.key - 48)

    def draw(self):
        """
        Draws on the screen
        """
        self.screen.fill(white())

        self.armor.draw()
        for target in self.targets:
            target.draw()
        for b in self.balls:
            b.draw()

        self.draw_score()
        self.draw_stats()

        pygame.display.update()

    def login(self):
        """
        Takes user's nickname which he types by keyboard
        """

        while not self.logged:  # waiting for typing the nickname
            self.screen.fill(GRAY())

            log_text = pygame.font.Font(None, 72).render('Enter your name: '
                                                         + self.username,
                                                         True, WHITE())
            self.screen.blit(log_text, (10, 10))

            self.events()  # catches application's events

            pygame.display.update()

    def write_stats(self):
        """
        Updates users' statistics
        """
        is_new = True
        self.highscore = max(self.points, self.highscore)

        with open(self.database_path, 'r') as f:  # reading old statistics
            loaded = [i.split() for i in f.read().splitlines()]

        for i in range(len(loaded)):  # adding new data
            if loaded[i][0] == self.username and i != 0:
                loaded[i][1] = str(max(int(loaded[i][1]), int(self.highscore)))
                is_new = False
                break

        if is_new:  # if user is new, adding him
            loaded.append([self.username, str(int(self.highscore))])

        with open(self.database_path, 'w') as f:  # loading statistics to the file
            for i in loaded:
                for j in i:
                    f.write(j + ' ')
                f.write('\n')

    def draw_stats(self):
        # Writing rating list

        with open(self.database_path, 'r') as f:  # reading data
            loaded = [i.split() for i in f.read().splitlines()]
        del loaded[0]
        loaded = sorted(loaded, key=lambda x: x[1], reverse=True)  # sorting data

        for i, string in enumerate(loaded):  # writing each rank
            text = pygame.font.Font(None, 24).render(str(i + 1) + '. ' + string[0] +
                                                     ' ' + string[1],
                                                     True, BERLIN_LAZUR())
            self.screen.blit(text, (500, 10 + i * 20))

    def draw_score(self):
        score_text = pygame.font.Font(None, 36).render('Score: '
                                                       + str(int(self.points))
                                                       + '         '
                                                       + 'Upgrades at levels: 1, 3, 5',
                                                       True, black())
        self.screen.blit(score_text, (10, 10))

        level_text = pygame.font.Font(None, 36).render('Level: '
                                                       + str(int(self.level)),
                                                       True, black())
        self.screen.blit(level_text, (10, 30))

        percent = int((self.level - int(self.level)) * 100)

        percent_text = pygame.font.Font(None, 36).render('     '
                                                         + str(percent)
                                                         + '%',
                                                         True, black())
        self.screen.blit(percent_text, (10, 50))


class EventLogger:
    """
    Class that catches all events and write it to a file
    logger_path -- path to a file, where events are written
    """
    logger_path = 'events.txt'

    def __init__(self):
        """
        Initialization of the logger
        """
        self.write_event('EventLogger initialized')

    def write_event(self, text):
        """
        Basic event-write command, write time of the event and it's name
        text -- name of the event
        """
        date_now = str(datetime.datetime.now())

        with open(self.logger_path, 'a') as f:
            f.write(date_now + ' ' + text + '\n')

    def game_event(self, text):
        """
        Writes event bounded with the game
        text -- name of the event
        """
        self.write_event('Game ' + text)

    def button_event(self, text, typ):
        """
        Writes event bounded with buttons
        text -- name of the event
        typ -- 'ButtonDown' or 'ButtonUp', depends on what was done with button
        """
        if typ == 'ButtonDown':
            self.write_event('Pushed Button ' + text)
        elif typ == 'ButtonUp':
            self.write_event('Released Button ' + text)

    def mouse_event(self, text, button='Left'):
        """
        Writes mouse click event
        text -- name of the event
        button -- 'Left' or 'Right' button of the mouse
        """
        self.write_event('Pushed ' + button + 'MouseButton ' + text)

    def get_event(self, event):
        """
        Works with pygame events
        """
        typ = 'None'

        if event.type == pygame.QUIT:
            self.game_event('ended')
        elif event.type == pygame.KEYDOWN:
            typ = 'ButtonDown'
        elif event.type == pygame.KEYUP:
            typ = 'ButtonUp'

        if event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            if event.key == pygame.K_SPACE:
                self.button_event('Space', typ)
            elif event.key == pygame.K_UP:
                self.button_event('Up arrow', typ)
            elif event.key == pygame.K_DOWN:
                self.button_event('Down arrow', typ)
            elif event.key == pygame.K_LEFT:
                self.button_event('Left arrow', typ)
            elif event.key == pygame.K_RIGHT:
                self.button_event('Right arrow', typ)
            elif event.key == pygame.K_BACKSPACE:
                self.button_event('BACKSPACE', typ)
            elif event.key == 13:
                self.button_event('ENTER', typ)

            elif 97 <= event.key <= 122:
                letters = 'abcdefghijklmnopqrstuvwxyz'
                self.button_event(letters[event.key - 97], typ)
            elif 48 <= event.key <= 57:
                self.button_event(str(event.key - 48), typ)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                position = event.pos
                self.mouse_event(' at ' + str(position[0])
                                 + ' ' + str(position[1]))
