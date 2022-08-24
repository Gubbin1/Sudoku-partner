def findNextMove(cells, blocks):
    # Moves through methods in order of complexity, if progress is made return with the information.
    if not fillGreen(cells, blocks):
        pass
    else:
        return
    if not checkForFillableCells(cells):
        pass
    else:
        return "Elimination"
    if not hiddenSingle(cells, blocks):
        pass
    else:
        return "Hidden single"
    if not nakedPairs(cells, blocks):
        pass
    else:
        return "Naked Pair"

# Cells have their position in the cell array, their corresponding button, their possible values, and when answered their actual value.
class cell(): 
    def __init__(self, myRow, myColumn, myButton):
        self.row = myRow
        self.column = myColumn
        self.index = (myRow, myColumn)
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
    # When a cell's answer is found, remove its value from the possibilities of all related cells
    def updateRelated(self, cells, blocks):
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

            if thisRow == blocks[self.block][i][0] and blocks[self.block][i][1] == thisCol:
                pass
            elif self.value in cells[blocks[self.block][i][0]][blocks[self.block][i][1]].poss:
                cells[blocks[self.block][i][0]][blocks[self.block][i][1]].poss.remove(self.value)
    # When there is only one possibility, fill in value with that possibility. If the answer has been found by other means, display the answer and clear out the possibilities
    def fill(self):
        if self.value == None and len(self.poss) == 1:
            self.value = self.poss[0]
        self.poss.clear()
        self.entryButton.text = self.value
        self.entryButton.background_color = "white"
    
# Check the grid for the green cell and fills it. Cells are made green when they are next to be answered.
def fillGreen(cells, blocks):
    for i in range(9):
        for j in range(9):
            if cells[i][j].entryButton.background_color == [0, 1, 0, 1]:
                cells[i][j].fill()
                cells[i][j].updateRelated(cells, blocks)
                return True
    return False

# Looks for cells with only one possibility and colors the first one found green
def checkForFillableCells(cells):
    for i in range(9):
        for j in range(9):
            if len(cells[i][j].poss) == 1:
                cells[i][j].entryButton.background_color = (0, 1, 0, 1)
                return True
    return False

# Checks rows, columns, and blocks for cells where there is only one possible place for a given value
def hiddenSingle(cells, blocks):

    nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    keys = ["tl", "tm", "tr",
            "ml", "mm", "mr",
            "bl", "bm", "br"]

    cellRow = None
    cellCol = None
    # Checks rows for instances where a given value appears only once
    for group in cells:
        for n in nums:
            count = 0
            for i in range(9):
                if n == group[i].value or count > 1:
                    break
                if n in group[i].poss:
                    count += 1
                    cellRow = group[i].row
                    cellCol = i
            if count == 1:
                cells[cellRow][cellCol].entryButton.background_color = (0, 1, 0, 1)
                cells[cellRow][cellCol].value = n
                return True
    # Checks columns for instances where a given value appears only once
    for i in range(9):
        for n in nums:
            count = 0
            for j in range(9):
                if n == cells[j][i].value or count > 1:
                    break
                if n in cells[j][i].poss:
                    count += 1
                    cellRow = j
                    cellCol = i
            if count == 1:
                cells[cellRow][cellCol].entryButton.background_color = (0, 1, 0, 1)
                cells[cellRow][cellCol].value = n
                return True
    # Checks blocks for instances where a given value appears only once
    for block in keys:
        for n in nums:
            count = 0
            for i in range(9):
                if n == cells[blocks[block][i][0]][blocks[block][i][1]].value or count > 1:
                    break
                if n in cells[blocks[block][i][0]][blocks[block][i][1]].poss:
                    count += 1
                    cellRow = blocks[block][i][0]
                    cellCol = blocks[block][i][1]
            if count == 1:
                cells[cellRow][cellCol].entryButton.background_color = (0, 1, 0, 1)
                print(f"{cellRow}, {cellCol}, {n}")
                cells[cellRow][cellCol].value = n
                return True

# Checks rows, columns, and blocks for pairs of cells that share the same ONLY TWO possibilities, removes those possibilities from other related cells
def nakedPairs(cells, blocks):
    maybes = []
    found = False
    keys = ["tl", "tm", "tr",
            "ml", "mm", "mr",
            "bl", "bm", "br"]
    # Checks rows for cells with only two possibilities, stores them.
    for line in cells:
        for i in range(9):
            if len(line[i].poss) == 2:
                maybes.append(line[i])
        if len(maybes) > 1:
            found = checkPairs(maybes)
        if found != False:
            updateNakedPair((maybes[found[0]], maybes[found[1]]), cells, blocks)
            return True
        maybes.clear()
    # Checks columns for cells with only two possibilities, stores them.
    for j in range(9):
        for i in range(9):
            if len(cells[i][j].poss) == 2:
                maybes.append(cells[i][j])
        if len(maybes) > 1:
            found = checkPairs(maybes)
        if found != False:
            updateNakedPair((maybes[found[0]], maybes[found[1]]), cells, blocks)
            return True
        maybes.clear()
    # Checks blocks for cells with only two possibilities, stores them.
    for key in keys:
        for index in blocks[key]:
            if len(cells[index[0]][index[1]].poss) == 2:
                maybes.append(cells[index[0]][index[1]])
        if len(maybes) > 1:
            found = checkPairs(maybes)
        if found != False:
            updateNakedPair((maybes[found[0]], maybes[found[1]]), cells, blocks)
            return True
        maybes.clear()
    return False

# Goes through a list of cells, returns the first pair found.
def checkPairs(group):
    for i in range(len(group) - 1):
        temp = group[i].poss
        for j in range(1, len(group)):
            if temp == group[j].poss:
                return ((i, j))
    return False

# Clears possiilities for cells related to a pair
def updateNakedPair(pair, cells, blocks):
    pairRow = pair[0].row
    pairCol = pair[0].column
    pairBlock = pair[0].block
    # If the pair occurred in a row, clear related cells in the row
    if pairRow == pair[1].row:
        for i in range(9):
            for j in range(2):
                if cells[pairRow][i] not in pair and pair[0].poss[j] in cells[pairRow][i].poss:
                    cells[pairRow][i].poss.remove(pair[0].poss[j])
    # Otherwise if the pair occurred in a column, clear related cells from the column
    elif pairCol == pair[1].column:
        for i in range(9):
            for j in range(2):
                if cells[i][pairCol] not in pair and pair[0].poss[j] in cells[i][pairCol].poss:
                    cells[i][pairCol].poss.remove(pair[0].poss[j])
    # Pairs from rows or columns can also share a block, so always checks the blocks for pairs
    if pairBlock == pair[1].block:
        for index in blocks[pairBlock]:
            for j in range(2):
                if cells[index[0]][index[1]] not in pair and pair[0].poss[j] in cells[index[0]][index[1]].poss:
                    cells[index[0]][index[1]].poss.remove(pair[0].poss[j])

