def findNextMove(cells, blocks):
    if not fillGreen(cells, blocks):
        pass
    else:
        return
    if not checkForFillableCells(cells):
        pass
    else:
        return "Elimination"

class cell():
    def __init__(self, myRow, myColumn, myButton):
        self.row = myRow
        self.column = myColumn
        self.block = None
        self.poss = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.value = None
        self.entryButton = myButton
        if 0 <= self.row < 3 and 0 <= self.column < 3:
            self.block = "tl"
        elif 0 <= self.row < 3 and 2 < self.column < 6:
            self.block = "tm"
        elif 0 <= self.row < 3 and 5 < self.column < 9:
            self.block = "tr"
        elif 2 < self.row < 6 and 0 <= self.column < 3:
            self.block = "ml"
        elif 2 < self.row < 6 and 2 < self.column < 6:
            self.block = "mm"
        elif 2 < self.row < 6 and 5 < self.column < 9:
            self.block = "mr"
        elif 5 < self.row < 9 and 0 <= self.column < 3:
            self.block = "bl"
        elif 5 < self.row < 9 and 2 < self.column < 6:
            self.block = "bm"
        elif 5 < self.row < 9 and 5 < self.column < 9:
            self.block = "br"

    def updateRelated(self, cells, blocks):
        bugtest = 0
        thisRow = self.row
        thisCol = self.column
        for i in range(9):
            if i == thisRow:
                pass
            elif self.value in cells[i][self.column].poss:
                cells[i][self.column].poss.remove(self.value)

            if i == thisCol:
                pass
            elif self.value in cells[self.row][i].poss:
                cells[self.row][i].poss.remove(self.value)

            if blocks[self.block][i].row == thisRow and blocks[self.block][i].column == thisCol:
                pass
            elif self.value in blocks[self.block][i].poss:
                blocks[self.block][i].poss.remove(self.value)

    def fill(self):
        self.value = self.poss[0]
        self.poss.clear()
        self.entryButton.text = self.value
        self.entryButton.background_color = "white"

def fillGreen(cells, blocks):
    for i in range(9):
        for j in range(9):
            if cells[i][j].entryButton.background_color == [0, 1, 0, 1]:
                cells[i][j].fill()
                cells[i][j].updateRelated(cells, blocks)
                return True
    return False

def checkForFillableCells(cells):
    for i in range(9):
        for j in range(9):
            if len(cells[i][j].poss) == 1:
                cells[i][j].entryButton.background_color = (0, 1, 0, 1)
                return True
    return False