import random

from enemy import Enemy
# Class for creating a group of red enemies
class Group():
    def __init__(self):
        self.ypos = random.randint(0,100)

        self.enemylist = self.addenemies()
        self.count = 5

    # Simple method for adding red enemies into the group class
    def addenemies(self):
        xpos = 0
        templist = []
        for x in range(5):
            ren1 = Enemy(True, xpos, self.ypos)
            templist.append(ren1)
            xpos -= 50
        return templist

