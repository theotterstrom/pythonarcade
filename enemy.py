import math
import time
import pyxel

class Enemy():
    def __init__(self, red: bool, x: int, y: int):
        self.x = x
        self.y = y
        self.sprite = (0, 0, 0, 16, 16)
        self.red = red
        # Bool for when easy enemies turn bacl
        self.turn = False
        # Bool for when red enemies loop
        self.loop = False
        # Bool for handling the loop
        self.tempbool = False
        # The amount of iterations of the loop that has gone
        self.loopcount = 0
        # Bool for when the loop is finished
        self.loopfinish = False
        # Circle coordinates for the red enemy
        self.circlecoo = self.circle(85, self.y)
        self.spritelist = [(1,24,48,18,18), (1,32,32,18,18), (1,16,32,18,18)]
        if red:
            self.sprite = (1, 0, 32, 16, 16)
            self.lives = 3
        else:
            self.sprite = (1,16,16,16,16)
            self.lives = 1

    # Method for moving the enemies
    def move(self):
        # Easy enemy movement, goes to 127.5 of Y and then turns back
        if not self.red:
            if self.y < 127.5 and not self.turn:
                self.y += 2
            else:
                self.turn = True
                self.sprite = (1,0,16,16,16)
                self.y -= 2
        else:
            # First distance, going to X = 85 before doing a loop, because the loop takes the player back some pixels from X = 85
            # self.loop is required
            if self.x < 85 and not self.loop:
                self.x += 3
            else:
                self.loop = True

            # If it is time to loop
            if self.loop:

                # first part of the loop
                if self.loopcount < 40 and not self.tempbool:
                    if self.loopcount < 20:
                        self.sprite = self.spritelist[0]
                    else:
                        self.sprite = self.spritelist[1]
                        # First X-coordinated within self.circlecoo
                    self.x = self.circlecoo[self.loopcount][0]
                    self.y = self.circlecoo[self.loopcount][2]
                    self.loopcount += 1
                # when loopcount reaches above 40, the second X-coordinated from self.circlecoo are required
                else:
                    if self.loopcount > 0:
                        self.sprite = self.spritelist[2]
                        # tempbool for stopping the program of going in to the first X-coordinates
                        self.tempbool = True
                        # Second X-coordinated within self.circlecoo
                        self.x = self.circlecoo[self.loopcount][1]
                        self.y = self.circlecoo[self.loopcount][2]
                        self.loopcount -= 1
                        # The second loop, happening at x = 150
                    else:
                        if self.x > 150 and not self.loopfinish:
                            # we create new coordinates for the loop starting at x = 150
                            self.circlecoo = self.circle(150, self.y)
                            # reset loopcount, tempbool, set looping to true and loopfinish indicating it is the last loop we will do
                            self.loopcount = 0
                            self.tempbool = False
                            self.loop = True
                            self.loopfinish = True
                        else:
                            self.sprite = (1, 0, 32, 15, 16)
                            self.x += 3


    # Method for getting coordinates for the loops, taking the coordinates for x and y and returning a list of the circle-coordinates
    def circle(self, xc: int, yc: int):
        r = 20
        newlist = []
        start = yc - r
        stop = yc + r + 1
        for x in range(start, stop):
            tv = math.pow(xc, 2)
            tu = math.pow((start - yc), 2)
            tx = math.pow(r, 2)
            tp = xc
            x1 = xc + int(math.sqrt(math.pow(xc, 2) - tv - tu + tx))
            x2 = xc - int(math.sqrt(math.pow(xc, 2) - tv - tu + tx))
            y = start + 20
            newlist.append((x1, x2, y))
            start += 1
        return newlist