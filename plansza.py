class HexGrid:

    def __init__(self,x,y):
        self.xSize = x
        self.ySize = y
        self.zajete = {}
        for i in range(x):
            for j in range(y):
                self.zajete[str(i)+str(j)] = 0

    def czyZajete(self,x,y):
        return self.zajete[str(x)+str(y)]

    def rysuj(self):
        powtX = (self.xSize + 1) // 2
        tmp = ''
        for i in range(powtX):
            tmp += ' _  '
        print tmp
        for j in range(self.ySize):
            tmp = ''
            if j % 2 == 0:
                for i in range(powtX):
                    tmp += '/'
                    if self.czyZajete(2*i,j):
                        tmp += 'X'
                    else:
                        tmp += ' '
                    tmp += '\_'
                tmp = tmp[0:-1]
            if j % 2 == 1:
                for i in range(powtX):
                    tmp += '\_/'
                    if self.czyZajete(2*i+1,j+1):
                        tmp += 'X'
                    else:
                        tmp += ' '
            print tmp

