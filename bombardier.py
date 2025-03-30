class Bombardier():
    def __init__(self, big: bool, x: int, y: int):
        self.x = x
        self.y = y
        # Boolean used for the small bombardier returning
        self.back = False
        # Boolean for deciding if big bombardier or not
        self.big = big
        if big:
            self.sprite = (1, 32, 64, 64, 56)
            self.lives = 8
        else:
            self.sprite = (0, 0, 216, 40, 24)
            self.lives = 4

    # Method for moving the bombardiers, big ones go one way
    def move(self):
        if self.big:
            self.y -= 1
        else:
            if self.back:
               # 3rd distance, when small bombardier is returning back
               if self.y > 115:
                   self.sprite = (0,168,216,32,32)
               elif self.y > 110:
                   self.sprite = (0,200,216,32,32)
               else:
                   self.sprite = (1, 0, 72, 30, 25)
               self.y -= 2
               # 1st distance when going down
            elif self.y < 120:
                if self.y > 115:
                    self.sprite = (0,48,216,28,32)
               # 1
                self.y += 2
            elif self.x < 180:
                if self.x < 5:
                    self.sprite = (0, 77, 216, 30, 32)
                if self.x < 10:
                    # 3
                    self.sprite = (0, 112, 216, 24, 32)
                else:
                    self.sprite = (0,141,216,25,30)
                # 2nd distance when moving horizontally
                self.x += 2
            else:
                self.back = True

    # Method for changing the sprites depending on the amount of damage
    def damageSprite(self):
        if self.big:
            if self.lives == 6:
                self.sprite = (0,144,96,64,56)
            elif self.lives == 4:
                self.sprite = (0,72,96,64,56)
            elif self.lives == 2:
                self.sprite = (0, 136, 40, 68, 48)