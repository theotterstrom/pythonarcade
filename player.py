import math
from datetime import datetime

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.sprite = (1, 0, 111, 30, 16)
        self.lives = 3
        # Boolean for checking if the player is currently looping
        self.loop = False
        self.loopcount = 3
        # empty value later declared with datetime for checking when the loop started
        self.loopstart = 0
        self.bonusstart = 0
        self.score = 0
        self.bonus = 8

    # Method for moving the player
    def move(self, direction: str, size: int):
        plane_x_size = self.sprite[3]
        plane_y_size = self.sprite[4]
        if direction.lower() == 'right' and self.x < size - plane_x_size:
            self.x = self.x + 3
        elif direction.lower() == 'left' and self.x > 0:
            self.x -= 3
        elif direction.lower() == 'up' and self.y > 0:
            self.y -= 3
        elif direction.lower() == 'down' and self.y < size - plane_y_size:
            self.y += 3

    # Method for handling the collisions of enemies
    def collisionHandlerEnemy(self, activenmy: list):
        # We "draw" the player mathematically by using range from start x & y + the size
        plxrange = range(math.floor(self.x), math.floor(self.x + 16))
        plyrange = range(math.floor(self.y), math.floor(self.y + 16))
        # We create a set from the range for later use when checking if the player intersects with the enemy
        xset = set(plxrange)
        yset = set(plyrange)
        # We loop over active enemies and do the same range/set functions
        for item in activenmy:
            enxrange = range(item.x, item.x + 16)
            enyrange = range(item.y, item.y + 16)
            # If the list of intersecting sets are larger than one on both Y & X, there is a collision
            if len(xset.intersection(enxrange)) > 0 and len(yset.intersection(enyrange)) > 0:

                return True

    # Same as previous method
    def collisionHandlerBomb(self, activebomb: list):
        plxrange = range(math.floor(self.x), math.floor(self.x + 16))
        plyrange = range(math.floor(self.y), math.floor(self.y + 16))
        xset = set(plxrange)
        yset = set(plyrange)
        for item in activebomb:
            if item.big:
                enxrange = range(item.x, item.x + 64)
                enyrange = range(item.y, item.y + 56)
            else:
                enxrange = range(item.x, item.x + 40)
                enyrange = range(item.y, item.y + 24)
            if len(xset.intersection(enxrange)) > 0 and len(yset.intersection(enyrange)) > 0:

                return True

    # Same as previous method
    def collisionHandlerShot(self, activeshot: list):
        plxrange = range(math.floor(self.x), math.floor(self.x + 16))
        plyrange = range(math.floor(self.y), math.floor(self.y + 16))
        xset = set(plxrange)
        yset = set(plyrange)
        for item2 in activeshot:
            # Except we are checking if the fire is hostile
            if not item2.ff:
                shxrange = range(math.floor(item2.x), math.floor(item2.x)+5)
                shyrange = range(math.floor(item2.y), math.floor(item2.y)+5)
            try:
                if len(xset.intersection(shxrange)) > 0 and len(yset.intersection(shyrange)) > 0 and not self.loop:

                    return True
            except:
                None

    # We set loopstart and change sprite according to the loop
    def loopdef(self):
        self.loopstart = datetime.now()
        self.sprite = (1, 0, 130, 32, 14)
        self.loop = True

    # We check if the time passed between the start of the loop and the current time is equal to one
    def loopcheck(self):
        calctime = datetime.now() - self.loopstart
        if calctime.seconds == 1:
            # If so, we exit the loop
            self.loopcount -= 1
            self.loop = False
            self.sprite = (1, 0, 111, 30, 16)

    # We check if the bonus is active, if so, if it has been lasting for three seconds, we set it back to normal
    def bonusTimeout(self):
        if self.score == 50:
            self.loopcount += 3
        if self.bonus == 2:
            calctime = datetime.now() - self.bonusstart
            if calctime.seconds == 3:
                self.bonus = 8