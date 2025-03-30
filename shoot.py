class Shoot():
    def __init__(self, startpos: tuple, targetpos: tuple, ff: bool):
        self.startpos = startpos
        self.targetpos = targetpos
        self.x = startpos[0]
        self.y = startpos[1]
        # Equation of fetching variable K, M, change in X, change in Y. Used for self.linelist
        self.equation = self.geteq(startpos, targetpos)
        self.sprite = (1,40,0,12,8)
        self.linecount = 0
        # Fetching a list of positions for target-seeking shots, using the attribute self.equation
        self.linelist = self.getposlist()
        # Deciding if the shot is friendly or not
        self.ff = ff

    # Method for moving the shots
    def move(self):
        # Friendly fire simply moves up
        if self.ff:
            self.y -= 4
            self.x = self.x
        # Enemy fire moves according to the equation fetched from self.getposlist
        else:
            try:
                self.x = self.linelist[self.linecount][0]
                self.y = self.linelist[self.linecount][1]
            except:
                None
            self.linecount += 1

    # Method for calculating the straight lines equation
    def getposlist(self):
        k = self.equation[0]
        m = self.equation[1]
        cx = self.equation[2]
        cy = self.equation[3]

        poslist = []
        # First position is where the shot is actually at right now
        poslist.append((self.x, self.y))
        # shot goes right
        if self.targetpos[0] > self.startpos[0]:
            # shot goes down
            if self.targetpos[1] > self.startpos[1]:
                # upper slice
                if self.targetpos[0] > self.targetpos[1]:
                    xval1 = self.x

                    for x in range(255):
                        yval1 = k * xval1 + m
                        poslist.append((xval1, yval1))
                        xval1 += 2

                # bottom slice
                elif self.targetpos[1] > self.targetpos[0]:
                    yval2 = self.y
                    for x in range(255):
                        xval2 = (yval2 / k) - (m / k)
                        poslist.append((xval2, yval2))
                        yval2 += 2


            # shot goes up
            elif self.startpos[1] > self.targetpos[1]:
                # bottom slice
                if self.targetpos[0] + self.targetpos[1] > 255:
                        xval1 = self.x
                        for x in range(255):
                            yval1 = k * xval1 + m
                            tempy = 125 - (yval1 - 125)
                            poslist.append((xval1, tempy))
                            xval1 += 2

                # upper slice
                else:
                    yval2 = self.y
                    for x in range(255):
                        xval2 = (yval2 / k) - (m / k)
                        tempy = 125 - (yval2 - 125)
                        poslist.append((xval2, tempy))
                        yval2 += 2

        # shot goes left
        elif self.startpos[0] > self.targetpos[0]:
            # shot goes down
            if self.targetpos[1] > self.startpos[1]:
                # upper slice
                if self.targetpos[0] + self.targetpos[1] > 255:
                    yval2 = self.y
                    for x in range(500):
                        xval2 = (yval2 / k) - (m / k)
                        tempx = 125 - (xval2 - 125)
                        poslist.append((tempx, yval2))
                        yval2 += 2

                # bottom slice
                elif self.targetpos[1] > self.targetpos[0]:
                    xval1 = self.x
                    for x in range(500):
                        yval1 = k * xval1 + m
                        tempx = 125 - (xval1 - 125)
                        poslist.append((tempx, yval1))
                        xval1 += 2


            # shot goes up
            elif self.startpos[1] > self.targetpos[1]:
                # bottom slice
                if self.targetpos[1] > self.targetpos[0]:
                    xval1 = self.x
                    for x in range(500):
                        yval1 = k * xval1 + m
                        tempx = 125 - (xval1 - 125)
                        tempy = 125 - (yval1 - 125)
                        poslist.append((tempx, tempy))
                        xval1 += 2

                # upper slice
                else:
                    yval2 = self.y
                    for x in range(500):
                        xval2 = (yval2 / k) - (m / k)
                        tempx = 125 - (xval2 - 125)
                        tempy = 125 - (yval2 - 125)
                        poslist.append((tempx, tempy))
                        yval2 += 2
        return poslist

    # Method for fetching the value K(the tilt of the line) M(where the line cuts the axis) change in Y and change in X
    # in order to reach the player from the enemy
    def geteq(self, spos, tpos):
        changex = 0
        changey = 0

        sposx = spos[0] #start x
        sposy = spos[1] #start y
        tposx = tpos[0] #mål x
        tposy = tpos[1] #mål y

        while sposx > tposx:
            changex += 1
            sposx -= 1
        while sposx < tposx:
            changex += 1
            sposx += 1
        while sposy > tposy:
            changey += 1
            sposy -= 1
        while sposy < tposy:
            changey += 1
            sposy += 1
        k = changey / changex
        mval = self.startpos[1] - (k * self.startpos[0])

        return (k, mval, changex, changey)