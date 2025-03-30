import math
import random
from enemy import *
from group import *
from bombardier import *
from shoot import *
from player import Player
from datetime import datetime

# Class events is for handling the events regarding shots, enemies killed and to generate random enemies and shots
class Events:
    def __init__(self, player: Player):
        self = self
        # Boolean list switching on/off when one type of enemy is currently present on the screen
        self.busy = [False, False, False, False]
        self.player = player
        self.group = []


    # Method for handling shot-events
    def shotHandler(self, activeshots: list, activenmy: list, activebomb: list, player: Player):
        # Fetching all the positions of enemies and shots
        shotpos = self.shotHandlerShot(activeshots)
        enempos = self.shotHandlerEnemy(activenmy)
        bombpos = self.shotHandlerBomb(activebomb)

        # For every active shot we check if it kills the enemy or not, if not we return 0
        for item2 in shotpos:
            try:
                if activeshots[item2[2]].ff:
                    if self.enemykilled(enempos, item2, activeshots, activenmy):
                        # 1 point
                        return 1
                    if self.bombkilled(bombpos, item2, activeshots, activebomb):
                        # 5 points
                        return 5

            except:
                None
        return 0

    # Function for fetching all the bombardier positions
    def shotHandlerBomb(self, activebomb: list):
        bombpos = []
        m = 0
        for bomb in activebomb:
            # We create a range, drawing out the entire rectangle of either small bombardier or big
            if bomb.big:
                bmxrange = range(bomb.x, bomb.x + 70)
                bmyrange = range(bomb.y, bomb.y + 20)
            else:
                bmxrange = range(bomb.x, bomb.x + 30)
                bmyrange = range(bomb.y, bomb.y + 10)

            # We create a tuple consisting of the sets of the range, this is for checking the intersection of the rectangles
            bombpos.append((set(bmxrange), set(bmyrange), m))
            m += 1
        return bombpos

    # Same as with shotHandlerBomb but with the enemies (red and normal enemies are the same size)
    def shotHandlerEnemy(self, activenmy: list):
        enempos = []
        i = 0
        for item in activenmy:
            enxrange = range(item.x, item.x + 16)
            enyrange = range(item.y, item.y + 16)
            enempos.append((set(enxrange), set(enyrange), i))
            i += 1
        return enempos

    # Same as with shotHandlerBomb but with the shots
    def shotHandlerShot(self, activeshots: list):
        shotpos = []
        v = 0
        for shot in activeshots:
            shxrange = range(math.floor(shot.x - 2.5), math.floor(shot.x + 12))
            shyrange = range(math.floor(shot.y - 2.5), math.floor(shot.y + 8))
            shotpos.append((set(shxrange), set(shyrange), v))
            v += 1
        return shotpos

    # Method for checking the collisions of shots with the enemies
    def enemykilled(self, enempos: list, item2: int, activeshots: list, activenmy: list):
        for item3 in enempos:
            # item2[0] represents the X-set of a shot, item2[1] the Y-set
            # item3[0] represents the X-set of the enemy, item3[1] the Y-set
            # If the length of the intersection-list between shot and enemy either for X and Y is larger than 0
            # -that means the enemy got hit by a shot
            if len(item2[0].intersection(item3[0])) > 0 and len(item2[1].intersection(item3[1])) > 0:
                # we remove the shot
                activeshots.remove(activeshots[item2[2]])
                # decrease the lives of the enemy by one
                activenmy[item3[2]].lives -= 1
                # boolean if the enemy is red
                enemyisred = activenmy[item3[2]].red
                # if the enemy lives equals 0 we remove the enemy and return true so that the player score increases
                if activenmy[item3[2]].lives == 0:
                    activenmy.remove(activenmy[item3[2]])
                    # if the enemy is red and the group count equals 0, the player gets a bonus
                    if enemyisred:
                        self.group.count -= 1
                        if self.group.count == 0:
                            # the integer 2 represents the modula of pyxel frame rate in which the player can shoot
                            # the lesse the integer, the more shots he/she can shoot per frame
                            self.player.bonus = 2
                            self.player.bonusstart = datetime.now()
                    return True

    # Method for checking collisions of shots with the bombardiers
    def bombkilled(self, bombpos: list, item2: int, activeshots: list, activebomb: list):
        for item4 in bombpos:
            if len(item2[0].intersection(item4[0])) > 0 and len(item2[1].intersection(item4[1])) > 0:
                activeshots.remove(activeshots[item2[2]])
                activebomb[item4[2]].lives -= 1
                activebomb[item4[2]].damageSprite()
                if activebomb[item4[2]].lives == 0:
                    activebomb.remove(activebomb[item4[2]])
                    return True

    # Method delegating the spawning of enemies
    def generate_enemies(self, activenmy: list, activebomb: list, totsec: int):
        self.generate_normal_enemies(totsec, activenmy)
        self.generate_bombardier(totsec, activebomb)

    # Method for generating enemies
    def generate_normal_enemies(self, totsec: int, activenmy: list):
        n1 = random.randint(1, 5)
        n2 = n1 + 5
        if totsec % 10 == n1 and not self.busy[0]:
            self.busy[0] = True
            # spawn a random number of simple enemies from 0 to 4
            nrofenemy = random.randint(0, 4)
            for x in range(nrofenemy):
                x = Enemy(False, random.randint(10, 240), 0)
                activenmy.append(x)

        # Generates a group of red enemies
        if totsec % 10 == n2 and not self.busy[1]:
            self.busy[1] = True
            # We create a group of them
            gr1 = Group()
            self.group = gr1
            for x in range(5):
                activenmy.append(self.group.enemylist[x])

    # Method for generating bombardiers
    def generate_bombardier(self, totsec: int, activebomb: list):
        n3 = 5
        n4 = 8
        # Generates a bombardier
        if totsec % 10 == n3 and not self.busy[2]:
            self.busy[2] = True
            x = Bombardier(False, 0, 0)
            activebomb.append(x)

        # Generates a big bombardier
        if totsec % 10 == n4 and not self.busy[3]:
            self.busy[3] = True
            x = Bombardier(True, random.randint(50, 150), 255)
            activebomb.append(x)

    # Method for delegating the generation of random shots from random enemies
    def generate_shots(self, activenmy: list, activebomb: list, activeshots: list, totsec: int):
        # Random integer for choosing which type of enemy the shot should belong to
        type = random.randint(0,3)
        # normal enemy
        if type == 0 and len(activenmy) > 0:
            self.genShotEN(activenmy, activeshots)
       # red enemy
        elif type == 1 and len(activenmy) > 0:
           self.genShotREN(activenmy, activeshots)

        # small bombardier
        elif type == 2 and len(activebomb) > 0:
            self.genShotSmallB(activebomb, activeshots)
        # big bombardier
        elif type == 3 and len(activebomb)> 0:
           self.genShotBigB(activebomb, activeshots)

    # Method for generating easy enemy shots
    def genShotEN(self, activenmy: list, activeshots: list):
        if pyxel.frame_count % 5 == 0:
            try:
                # We create the index for choosing a random enemy from the list of active enemies
                index = random.randint(0, len(activenmy))
                # While this enemy is red, we keep on looking for an enemy who isn't
                while activenmy[index].red:
                    index = random.randint(0, len(activenmy))

                # Finally we have found a normal enemy in the list and takes that enemies position and append a shot to it
                tempen = activenmy[index]
                tempshot = Shoot((tempen.x, tempen.y), (self.player.x, self.player.y), False)

                activeshots.append(tempshot)
            except:
                None

    # Method for generating red enemy shots
    def genShotREN(self, activenmy: list, activeshots: list):
        if pyxel.frame_count % 30 == 0:
            try:
                index = 0
                while not activenmy[index].red:
                    index += 1
                tempen = activenmy[index]
                tempshot = Shoot((tempen.x, tempen.y), (self.player.x, self.player.y), False)
                activeshots.append(tempshot)
            except:
                None

    # Method for generating small bombardier shots
    def genShotSmallB(self, activebomb: list, activeshots: list):
        if pyxel.frame_count % 10 == 0:
            try:
                index = 0
                while activebomb[index].big:
                    index += 1
                tempbomb = activebomb[index]
                tempshot2 = Shoot((tempbomb.x, tempbomb.y), (self.player.x, self.player.y), False)
                activeshots.append(tempshot2)
            except:
                None

    # Method for generating big bombardier shots
    def genShotBigB(self, activebomb: list, activeshots: list):
        if pyxel.frame_count % 10 == 0:
            try:
                index = 0
                while not activebomb[index].big:
                    index += 1
                tempbomb = activebomb[index]
                # It shoots two shots
                tempshot2 = Shoot((tempbomb.x, tempbomb.y), (self.player.x, self.player.y), False)
                tempshot3 = Shoot((tempbomb.x, tempbomb.y - 5), (self.player.x, self.player.y), False)
                activeshots.append(tempshot2)
            except:
                None
