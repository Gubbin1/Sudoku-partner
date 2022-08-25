from unittest.mock import NonCallableMagicMock


def findNextMove(puzz):
    fl = [fillGreen, nakedSingle, hiddenSingle, nakedPairs, lockedCandidate, pointingTuple, hiddenPairs, nakedTriples]
    check = None
    # Moves through methods in order of complexity, if progress is made return with the information.
    for f in fl:
        check = f(puzz)
        if check[0]:
            return check[1]

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
    def updateRelated(self, puzz):
        thisRow = self.row
        thisCol = self.column
        for i in range(9):
            if i == thisRow:
                pass
            elif self.value in puzz.cells[i][self.column].poss:
                puzz.cells[i][self.column].poss.remove(self.value)

            if i == thisCol:
                pass
            elif self.value in puzz.cells[self.row][i].poss:
                puzz.cells[self.row][i].poss.remove(self.value)

            if thisRow == puzz.blockDic[self.block][i][0] and puzz.blockDic[self.block][i][1] == thisCol:
                pass
            elif self.value in puzz.cells[puzz.blockDic[self.block][i][0]][puzz.blockDic[self.block][i][1]].poss:
                puzz.cells[puzz.blockDic[self.block][i][0]][puzz.blockDic[self.block][i][1]].poss.remove(self.value)
    # When there is only one possibility, fill in value with that possibility. If the answer has been found by other means, display the answer and clear out the possibilities
    def fill(self):
        if self.value == None and len(self.poss) == 1:
            self.value = self.poss[0]
        self.poss.clear()
        self.entryButton.text = self.value
        self.entryButton.background_color = "white"
    # Clears out all but the values in a given list from possible
    def updateHidden(self, found):
        removed = []
        for n in self.poss:
            if n in found:
                pass
            else:
                self.poss.remove(n)
                removed.append(n)
        if len(removed) > 0:
            return True
        return False


class puzzle():
    def __init__(self):
        self.cells = [[None for i in range(9)] for j in range(9)]
        self.blockDic = {"tl": [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)], "tm": [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)], "tr": [(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)],
                "ml": [(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)], "mm": [(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)], "mr": [(3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)],
                "bl": [(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2)], "bm": [(6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)], "br": [(6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8)]}
        self.blockKeys = ["tl", "tm", "tr",
            "ml", "mm", "mr",
            "bl", "bm", "br"]
        self.rows = []
        self.columns = []
        self.blocks = []
        self.nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in range(9):
            row = []
            column = []
            for j in range(9):
                row.append((i, j))
                column.append((j, i))

            self.rows.append(row)
            self.columns.append(column)
            self.blocks.append(self.blockDic[self.blockKeys[i]])

    def index(self, coordinates):
        return self.cells[coordinates[0]][coordinates[1]]

# Check the grid for the green cell and fills it. Cells are made green when they are next to be answered.
def fillGreen(puzz):
    info = None
    for i in range(9):
        for j in range(9):
            if puzz.cells[i][j].entryButton.background_color == [0, 1, 0, 1]:
                puzz.cells[i][j].fill()
                puzz.cells[i][j].updateRelated(puzz)
                info = ["Fill Green"]
                return [True, info]
    return [False]

# Looks for cells with only one possibility and colors the first one found green
def nakedSingle(puzz):
    for i in range(9):
        for j in range(9):
            if len(puzz.cells[i][j].poss) == 1:
                puzz.cells[i][j].entryButton.background_color = (0, 1, 0, 1)
                return [True, "Naked Single"]
    return [False]

# Checks rows, columns, and blocks for cells where there is only one possible place for a given value
def hiddenSingle(puzz):
    info = None
    if not searchHiddenSingles(puzz.rows, puzz):
        pass
    else:
        info = ["Hidden Single", "Row"] 
        return [True, info]
    if not searchHiddenSingles(puzz.columns, puzz):
        pass
    else:
        info = ["Hidden Single", "Column"]  
        return [True, info]
    if not searchHiddenSingles(puzz.blocks, puzz):
        pass
    else: 
        info = ["Hidden Single", "Block"]  
        return [True, info]
    return [False]
    
# Defines the method for searching though a group of cells for a hidden single
def searchHiddenSingles(category, puzz):
    for group in category:
        for n in puzz.nums:
            count = 0
            found = None
            for i in range(9):
                if n == puzz.index(group[i]).value or count > 1:
                    break
                if n in puzz.index(group[i]).poss:
                    count += 1
                    found = group[i]
            if count == 1:
                puzz.cells[found[0]][found[1]].entryButton.background_color = (0, 1, 0, 1)
                puzz.cells[found[0]][found[1]].value = n
                return True
    return False

def pointingTuple(puzz):
    info = ["Pointing Tuple", None, []]
    for key in puzz.blockKeys:
        # Checks to see if all instances of a number in a block either appear in a single row or a single column
        for n in puzz.nums:
            Row = True
            Col = True
            lockedRow = None
            lockedCol = None
            holder = []
            count = 0
            for dex in puzz.blockDic[key]:
                if n in puzz.index(dex).poss:
                    holder.append(dex)
                    lockedRow = dex[0]
                    lockedCol = dex[1]
                    count += 1
                if count > 3:
                    count = 0
                    break
            if count > 1:
                for loc in holder:
                    if loc[0] != lockedRow:
                        Row = False
                    if loc[1] != lockedCol:
                        Col = False
                done = []
                if Row == True:
                    for dex in puzz.rows[lockedRow]:
                        if puzz.index(dex).block != key and n in puzz.index(dex).poss:
                            puzz.cells[dex[0]][dex[1]].poss.remove(n)
                            info[1] = "Row"
                            done.append(dex)
                    if len(done) > 0:
                        info[2] = done
                        return [True, info]
                elif Col == True:
                    for dex in puzz.columns[lockedCol]:
                        if puzz.index(dex).block != key and n in puzz.index(dex).poss:
                            puzz.cells[dex[0]][dex[1]].poss.remove(n)
                            info[1] = "Column"
                            done.append(dex)
                    if len(done) > 0:
                        info[2] = done
                        return [True, info]

    return [False]

def lockedCandidate(puzz):
    info = ["Locked Candidate"]
    if searchLockedCandidate(puzz.rows, puzz):
        info.append("Row")
        return [True, info]
    if searchLockedCandidate(puzz.columns, puzz):
        info.append("Column")
        return [True, info]
    return [False]

def searchLockedCandidate(category, puzz):
    for group in category:
        for n in puzz.nums:
            check = []
            found = []
            for dex in group:
                if n in puzz.index(dex).poss:
                    check.append(dex)
                elif n == puzz.index(dex).value or len(check) > 3:
                    check.clear()
                    break
            if len(check) > 1:
                temp = puzz.index(check[0]).block
                for dex in check:
                    if puzz.index(dex).block == temp:
                        found.append(dex)
                    else:
                        found.clear()
                        break
            if len(found) > 0:
                updated = []
                for dex in puzz.blockDic[puzz.index(found[0]).block]:
                    if dex not in found and n in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(n)
                        updated.append(puzz.cells[dex[0]][dex[1]])
                if len(updated) > 0:
                    return True
    return False

# Checks rows, columns, and blocks for pairs of cells that share the same ONLY TWO possibilities, removes those possibilities from other related cells
def nakedPairs(puzz):
    info = None
    if not searchNakedPairs(puzz.rows, puzz):
        pass
    else: 
        info = ["Naked Pair", "Row"]
        return [True, info]
    if not searchNakedPairs(puzz.columns, puzz):
        pass
    else: 
        info = ["Naked Pair", "Column"]
        return [True, info]
    if not searchNakedPairs(puzz.blocks, puzz):
        pass
    else: 
        info = ["Naked Pair", "Block"]
        return [True, info]
    return [False]

# Goes through a list of cells, returns the first pair found.
def searchNakedPairs(category, puzz):
    for group in category:
        maybes = []
        found = False
        for i in range(9):
            if len(puzz.index(group[i]).poss) == 2:
                maybes.append(puzz.index(group[i]))
        if len(maybes) > 1:
            found = checkPairs(maybes)
        if found != False:
            if updateNakedPair(found, puzz):
                return True
        maybes.clear()
    return False

def checkPairs(group):
    for i in range(len(group) - 1):
        temp = group[i].poss
        for j in range(i + 1, len(group)):
            if temp == group[j].poss:
                return ((group[i].index, group[j].index))
    return False

# Clears possiilities for cells related to a pair
def updateNakedPair(pair, puzz):
    cell1 = pair[0]
    cell2 = pair[1]
    pairValues = puzz.index(cell1).poss
    updated = []
    # If the pair occurred in a row, clear related cells in the row
    if cell1[0] == cell2[0]:
        for dex in puzz.rows[cell1[0]]:
            if dex != cell1 and dex != cell2:
                for i in range(2):
                    if pairValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(pairValues[i])
                        updated.append(dex)
    # Otherwise if the pair occurred in a column, clear related cells from the column
    elif cell1[1] == cell2[1]:
        for dex in puzz.columns[cell1[1]]:
            if dex != cell1 and dex != cell2:
                for i in range(2):
                    if pairValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(pairValues[i])
                        updated.append(dex)
    # Pairs from rows or columns can also share a block, so always checks the blocks for pairs
    if puzz.index(cell1).block == puzz.index(cell2).block:
        for dex in puzz.blockDic[puzz.index(cell1).block]:
            if dex != cell1 and dex != cell2:
                for i in range(2):
                    if pairValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(pairValues[i])
                        updated.append(dex)
    if len(updated) > 0:
        return True
    else:
        return False

def hiddenPairs(puzz):
    info = None
    if not searchHiddenPairs(puzz.rows, puzz):
        pass
    else: 
        info = ["Hidden Pair", "Row"]
        return [True, info]
    if not searchHiddenPairs(puzz.columns, puzz):
        pass
    else: 
        info = ["Hidden Pair", "Column"]
        return [True, info]
    if not searchHiddenPairs(puzz.blocks, puzz):
        pass
    else: 
        info = ["Hidden Pair", "Block"]
        return [True, info]
    return [False]
# Check rows, columns, and blocks for instances where two numbers are only available in two cells.
def searchHiddenPairs(category, puzz):
    numCount = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}
    maybes = []
    pairs = []
    found = None
    # Checks rows for hidden pairs
    for group in category:
        # Count up how many times each number is possible
        for n in puzz.nums:
            for i in range(9):
                if n in puzz.index(group[i]).poss:
                    numCount[n] += 1
        # Save the numbers with only two possible locations
        for n in puzz.nums:
            if numCount[n] == 2:
                maybes.append(n)
        # Put indexes of paired cells in an array, with number value
        if len(maybes) > 1:
            pairs = []
            for n in maybes:
                pair = []
                for i in range(9):
                    if n in puzz.index(group[i]).poss:
                        pair.append(group[i])
                pair.append(n)
                pairs.append(pair)
        # Check if any of the pairs match
        if len(pairs) > 1:
            for i in range(len(pairs) - 1):
                for j in range(i + 1, len(pairs)):
                    if pairs[i][0] == pairs[j][0] and pairs[i][1] == pairs[j][1]:
                        found = (pairs[i][2], pairs[j][2])
                        removed = 0
                        if puzz.cells[pairs[i][0][0]][pairs[i][0][1]].updateHidden(found):
                            removed += 1
                            puzz.cells[pairs[i][0][0]][pairs[i][0][1]].entryButton.background_color = (0, 0, 1, 1)
                        if puzz.cells[pairs[i][1][0]][pairs[i][1][1]].updateHidden(found):
                            removed += 1
                            puzz.cells[pairs[i][1][0]][pairs[i][1][1]].entryButton.background_color = (0, 0, 1, 1)
                        if removed > 0:
                            return True
        # Re-initialize starting values
        maybes.clear()
        pairs.clear()
        for key in puzz.nums:
            numCount[key] = 0
    return False

def nakedTriples(puzz):
    info = None
    if not searchNakedTriples(puzz.rows, puzz):
        pass
    else: 
        info = ["Naked Triple", "Row"]
        return [True, info]
    if not searchNakedTriples(puzz.columns, puzz):
        pass
    else: 
        info = ["Naked Triple", "Column"]
        return [True, info]
    if not searchNakedTriples(puzz.blocks, puzz):
        pass
    else: 
        info = ["Naked Triple", "Block"]
        return [True, info]
    return [False]

def searchNakedTriples(category, puzz):
    for group in category:
        maybes = []
        found = False
        for i in range(9):
            if 2 <= len(puzz.index(group[i]).poss) <= 3:
                maybes.append(puzz.index(group[i]))
        if len(maybes) > 2:
            found = checkTriples(maybes)
        if found != False:
            if updateNakedTriple(found, puzz):
                return True
        maybes.clear()
    return False

def checkTriples(group):
    length = len(group)
    cells = [None, None, None]
    for i in range(0, length - 2):
        for j in range (i + 1, length - 1):
            for k in range(j + 1, length):
                allPoss = []
                uniquePoss = []
                cells[0] = group[i]
                cells[1] = group[j]
                cells[2] = group[k]
                for x in range(3):
                    allPoss.extend(cells[x].poss)
                for x in allPoss:
                    if x not in uniquePoss:
                        uniquePoss.append(x)
                if len(uniquePoss) == 3:
                    return [cells[0].index, cells[1].index, cells[2].index]
    return False

def updateNakedTriple(trip, puzz):
    cells = [trip[0], trip[1], trip[2]]
    tripValues = []
    for dex in cells:
        for n in puzz.index(dex).poss:
            if n not in tripValues:
                tripValues.append(n)
    updated = []
    # If the triple occurred in a row, clear related cells in the row
    if cells[0][0] == cells[1][0] and cells[1][0] == cells[2][0]:
        for dex in puzz.rows[cells[0][0]]:
            if dex != cells[0] and dex != cells[1] and dex != cells[2]:
                for i in range(3):
                    if tripValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(tripValues[i])
                        updated.append(dex)
    # Otherwise if the triple occurred in a column, clear related cells from the column
    elif cells[0][1] == cells[1][1] and cells[1][1] == cells[2][1]:
        for dex in puzz.columns[cells[0][1]]:
            if dex != cells[0] and dex != cells[1] and dex != cells[2]:
                for i in range(3):
                    if tripValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(tripValues[i])
                        updated.append(dex)
    # Triples from rows or columns can also share a block, so always checks the blocks for triples
    if puzz.index(cells[0]).block == puzz.index(cells[1]).block and puzz.index(cells[1]).block == puzz.index(cells[2]).block:
        for dex in puzz.blockDic[puzz.index(cells[0]).block]:
            if dex != cells[0] and dex != cells[1] and dex != cells[2]:
                for i in range(3):
                    if tripValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(tripValues[i])
                        updated.append(dex)
    if len(updated) > 0:
        return True
    else:
        return False