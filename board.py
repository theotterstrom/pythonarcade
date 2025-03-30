from player import Player
from enemy import Enemy
from shoot import Shoot
from events import Events
from bombardier import Bombardier
from group import Group
import random
from datetime import datetime
import pyxel
import math
class Board:
    def __init__(self, w: int, h: int):
        self.width = w
        self.height = h
        pyxel.init(self.width, self.height, title="1942")
        pyxel.load("assets/my_resource.pyxres")
        self.player = Player(self.width / 2, 200)
        self.events = Events(self.player)
        self.activenmy = []
        self.activeshots = []
        self.activebomb = []
        self.starttime = datetime.now()
        # Booleans for creating "pause-modes" in which the player has to press space to play the game
        self.start = False
        self.nextLife = False
        self.bgcoordx = random.randint(50,200)
        self.bgcoordy = 0
        pyxel.run(self.update, self.draw)

    # Method for when the player looses lifes
    def restart(self):
        self.player.lives -= 1
        self.activeshots = []
        self.activebomb = []
        self.activenmy = []
        self.starttime = datetime.now()

        # If the players lives are equal to 0, the boolean is switched and the player is redirected to the start screen
        if self.player.lives == 0:
            self.start = False
            self.player.lives = 3
            self.player.score = 0

        else:
        # Else a screen shows which prompts the player to press space to try again
            self.nextLife = True

    def update(self):
        # If the player is not in either of these modes, the normal game will continute
        if self.start and not self.nextLife:
            # Methods calling the event-class for spawning random enemies and random shots
            self.events.generate_enemies(self.activenmy, self.activebomb, self.totsec())
            self.events.generate_shots(self.activenmy, self.activebomb, self.activeshots, self.totsec())
            # Calling a method for checking if the player is currently in bonus mode
            self.player.bonusTimeout()

            # If the length of either of these three lists are above 0, we will delegate to the update-functions
            if len(self.activeshots) > 0:
                self.updateShots()
            if len(self.activenmy) > 0:
                self.updateEnemies()
            if len(self.activebomb) > 0:
                self.updateBombardier()

            # If the player is currently in a loop, we have to check that the loop will stop after 1 second
            if self.player.loop:
                self.player.loopcheck()

            # To be able to shoot while pressing another key, the self.shoot() function is placed within each key-condition here
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.player.move('right', self.width)
                if pyxel.btn(pyxel.KEY_Z):
                    self.shoot()
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.player.move('left', self.width)
                if pyxel.btn(pyxel.KEY_Z):
                    self.shoot()
            elif pyxel.btn(pyxel.KEY_UP):
                self.player.move('up', self.height)
                if pyxel.btn(pyxel.KEY_Z):
                    self.shoot()
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.player.move('down', self.height)
                if pyxel.btn(pyxel.KEY_Z):
                    self.shoot()
            elif pyxel.btn(pyxel.KEY_Z):
                self.shoot()

            # Player loop checking if the player has any loops left to do
            elif pyxel.btn(pyxel.KEY_X):
                if self.player.loopcount > 0:
                    self.player.loopdef()

    # Method for updating the active shots
    def updateShots(self):
        for shot in self.activeshots:
            # If the shot is friendly fire (meaning the shot is from the player)
            if shot.ff:
                # Calling the method inside events-class checking if the player actually killed an enemy
                plusscore = self.events.shotHandler(self.activeshots, self.activenmy, self.activebomb, self.player)
                # If yes, we increase the score
                if plusscore > 0:
                    self.player.score += plusscore
            # If shot is of enemy origin
            else:
                # Calling a method inside player-class, checking if the shot is colliding with the player
                if self.player.collisionHandlerShot(self.activeshots):
                    self.restart()

            # Deleting the shots if they exit the screen
            if shot.x < 0 or shot.y < 0 or shot.x > 255 or shot.y > 255:
                try:
                    self.activeshots.remove(shot)
                except:
                    None
            # If the shot is within the screen, we delegate to make the shot move
            else:
                shot.move()

    # Method for updating the enemies
    def updateEnemies(self):
        # If a collision between player and enemy
        if self.player.collisionHandlerEnemy(self.activenmy):
            self.restart()
        else:
            for item in self.activenmy:
                # Delete enemy if outside the screen, varies depending on the kind of enemy
                if item.y < -5 or item.y > 250 or ((item.x < -5 or item.x > 250) and not item.red):
                    self.activenmy.remove(item)
                elif item.x > 250:
                    self.activenmy.remove(item)
                else:
                    item.move()

    # Method for updating the bombardier
    def updateBombardier(self):
        if self.player.collisionHandlerBomb(self.activebomb):
            self.restart()
        else:
            for item2 in self.activebomb:
                if item2.y < 0:
                    self.activebomb.remove(item2)
                else:
                    item2.move()

    # Method for the player shots
    def shoot(self):
        # The self.player.bonus represents the integer 5(normal mode) or 2(bonus mode)
        if pyxel.frame_count % self.player.bonus == 0:
            tempshot = Shoot((self.player.x, self.player.y), (255, self.player.y), True)
            self.activeshots.append(tempshot)

    # Method for drawing the game
    def draw(self):
        # Start screen
        if not self.start:
            pyxel.cls(0)
            pyxel.text(50, 50, "Welcome to 1942. Press space to start!", 5)
            # Press space to start the game, the boolean changes
            if pyxel.btn(pyxel.KEY_SPACE):
                self.start = True
                self.starttime = datetime.now()
        # If the player has been hit, a pause-mode is initated and an explosionis shows where the player is currently at
        elif self.nextLife:
            pyxel.blt(self.player.x, self.player.y, *(2, 216, 80, 16, 16), colkey=12)
            pyxel.text(50, 50, "You lost a life! Press space to try again!", 5)
            if pyxel.btn(pyxel.KEY_SPACE):
                self.nextLife = False
                self.player.y = 200
                self.player.x = self.width /2
        # Else the normal game proceeds
        else:
            pyxel.cls(12)
            self.background()
            pyxel.text(10, 10, "Seconds:", 0)
            pyxel.text(50, 10, str(self.totsec()), 0)
            pyxel.text(70, 10, "Score:", 0)
            pyxel.text(110, 10, str(self.player.score), 0)
            pyxel.text(130, 10, "Lives:", 0)
            pyxel.text(170, 10, str(self.player.lives), 0)
            pyxel.text(190, 10, "Loops:", 0)
            pyxel.text(220, 10, str(self.player.loopcount), 0)
            # We draw the enemies if the list is larger than 0
            if len(self.activenmy) > 0:
                for item2 in self.activenmy:
                    pyxel.blt(item2.x, item2.y, *item2.sprite, colkey=12)
            else:
                self.events.busy[0] = False
                self.events.busy[1] = False
            # Draw shots if list it larger than 0
            if len(self.activeshots) > 0:
                for item3 in self.activeshots:
                    # check if the shot if friendly fire or not
                    if item3.ff:
                        pyxel.blt(item3.x, item3.y, *item3.sprite)
                    else:
                        pyxel.blt(item3.x, item3.y, 1,37,20,7,5, colkey=12)
            if len(self.activebomb) > 0:
                for item4 in self.activebomb:
                    pyxel.blt(item4.x, item4.y, *item4.sprite, colkey=12)
            else:
                self.events.busy[2] = False
                self.events.busy[3] = False

            pyxel.blt(self.player.x, self.player.y, *self.player.sprite, colkey=12)


    # Timer used for some funtionalitites in the game
    def totsec(self):
        diff = datetime.now() - self.starttime
        return diff.seconds

    # Method for making the background move
    def background(self):
        if self.totsec() % 1 == 0:
            self.bgcoordy += 1
        if self.bgcoordy > 270:
            self.bgcoordy = -40
            self.bgcoordx = random.randint(50,200)

        pyxel.blt(self.bgcoordx, self.bgcoordy, *(1, 112, 24, 70, 60), colkey=12)

