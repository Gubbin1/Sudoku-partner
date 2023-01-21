from kivy.uix.anchorlayout import AnchorLayout

def findNextMove(puzz):
    fl = [fillGreen, nakedSingle, hiddenSingle, nakedPairs, lockedCandidate, pointingTuple, hiddenPairs, nakedTriples,
          hiddenTriples, Xwing, Ywing, simpleColoring]
    check = None
    # Moves through methods in order of complexity, if progress is made return with the information.
    for f in fl:
        check = f(puzz)
        if check[0]:
            return [True, check[1]]
    return [False, "Sorry, that's as far as I know."]

class Possibles(AnchorLayout):
    def __init__(self, **kwargs):
        super(Possibles, self).__init__(**kwargs)

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
        # self.possLayout = myPossLayout

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
        thisBlock = self.block
        value = self.value
        for i in range(9):
            # Clears value from possibles from the related row
            if value in puzz.cells[i][thisCol].poss:
                puzz.cells[i][thisCol].poss.remove(value)
            # Clears value from possibles from the related column
            if value in puzz.cells[thisRow][i].poss:
                puzz.cells[thisRow][i].poss.remove(value)
            # Clears value from possibles from the related block
            if self.value in puzz.cells[puzz.blockDic[thisBlock][i][0]][puzz.blockDic[thisBlock][i][1]].poss:
                puzz.cells[puzz.blockDic[thisBlock][i][0]][puzz.blockDic[thisBlock][i][1]].poss.remove(value)
    # When there is only one possibility, fill in value with that possibility. If the answer has been found by other means, display the answer and clear out the possibilities
    def fill(self):
        if self.value == None and len(self.poss) == 1:
            self.value = self.poss[0]
        self.poss.clear()
        self.entryButton.text = self.value
    # Clears out all but the values in a given list from possible
    def updateHidden(self, found):
        takeOut = []
        for n in self.poss:
            if n in found:
                pass
            else:
                takeOut.append(n)
        if len(takeOut) > 0:
            for n in takeOut:
                if n in self.poss:
                    self.poss.remove(n)
            return True
        return False
    # Returns true if a cell can "see" an index
    def sees(self, index, puzz):
        if self.index == index:
            return False
        elif self.row == index[0]:
            return True
        elif self.column == index[1]:
            return True
        elif index in puzz.blockDic[self.block]:
            return True
        return False

    def dependsOn(self, index, n, puzz):
        if self.index == index or n not in self.poss:
            return False
        if self.index[0] != index[0] and self.index[1] != index[1] and self.block != puzz.index(index).block:
            return False
        count = 0
        checkCell = None
        # Checks related row, column, and block for instances where "index" is the only other location with "n" as a possibility
        for i in range(9):
            if i != index[0]:
                if n in puzz.cells[i][index[1]].poss:
                    count += 1
                    checkCell = (i, index[1])
        if count == 1 and self.index == checkCell:
            return True
        count = 0
        checkCell = None
        for i in range(9):
            if i != index[1]:
                if n in puzz.cells[index[0]][i].poss:
                    count += 1
                    checkCell = (index[0], i)
        if count == 1 and self.index == checkCell:
            return True
        count = 0
        for blockMate in puzz.blockDic[puzz.index(index).block]:
            if blockMate != index:
                if n in puzz.index(blockMate).poss:
                    count += 1
                    if blockMate[0] != index[0] and blockMate[1] != index[1]:
                        checkCell = blockMate
        if count == 1 and checkCell == self.index:
            return True
        return False
        
# Holds all the necessary information for the entire puzzle
class puzzle():
    def __init__(self):
        self.cells = [[None for i in range(9)] for j in range(9)]
        self.remaining = 81
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
        self.complete = False
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
    
    def colorIn(self, *colorMe):
        allCoordinates = []
        for tup in colorMe:
            allCoordinates += tup[0]
            for coordinates in tup[0]:
                self.cells[coordinates[0]][coordinates[1]].entryButton.background_color = tup[1]
        for group in self.cells:
            for one in group:
                if one.index not in allCoordinates:
                    one.entryButton.background_color = [1, 1, 1, 1]

# Creates an object that holds all the information of a sudoku move
class history():
    # A dictionary that keeps a record of each move
    def __init__(self, method, cause, effect, num, category):
        self.record = {"method": method, "cause": cause, "effect": effect, "number": num, "category": category}

# Check the grid for the green cell and fills it. Cells are made green when they are next to be answered.
def fillGreen(puzz):
    info = None
    for i in range(9):
        for j in range(9):
            if puzz.cells[i][j].entryButton.background_color == [0, 1, 0, 1]:
                puzz.cells[i][j].fill()
                puzz.cells[i][j].updateRelated(puzz)
                puzz.remaining -= 1
                info = history("Fill In", (i, j), [], puzz.cells[i][j].value, "Cell")
                return [True, info]
    return [False]
# Looks for cells with only one possibility and colors the first one found green
def nakedSingle(puzz):
    info = None
    for i in range(9):
        for j in range(9):
            if len(puzz.cells[i][j].poss) == 1:
                info = history("Naked Single", [(i, j)], [], puzz.cells[i][j].poss[0], "Cell")
                return [True, info]
    return [False]
# Checks rows, columns, and blocks for cells where there is only one possible place for a given value
def hiddenSingle(puzz):
    info = None
    check = searchHiddenSingles(puzz.rows, puzz)
    if not check[0]:
        pass
    else:
        info = history("Hidden Single", check[1], [], check[2], "Row") 
        return [True, info]
    check = searchHiddenSingles(puzz.columns, puzz)
    if not check[0]:
        pass
    else:
        info = history("Hidden Single", check[1], [], check[2], "Column") 
        return [True, info]
    check = searchHiddenSingles(puzz.blocks, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Hidden Single", check[1], [], check[2], "Block") 
        return [True, info]
    return [False]  
# Defines the method for searching though a group of cells for a hidden single
def searchHiddenSingles(category, puzz):
    for group in category:
        for n in puzz.nums:
            count = 0
            found = []
            for i in range(9):
                if n == puzz.index(group[i]).value or count > 1:
                    break
                if n in puzz.index(group[i]).poss:
                    count += 1
                    found.append(group[i])
            if count == 1:
                puzz.cells[found[0][0]][found[0][1]].value = n
                return [True, found, n]
    return [False]
# Looks for places where numbers occuring in a block all exist in the same row or column, allowing for eliminations in the remainder of the row or column
def pointingTuple(puzz):
    info = ["Pointer", None, [], None]
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
                        hist = history(info[0], holder, info[2], n, info[1])
                        return [True, hist]
                elif Col == True:
                    for dex in puzz.columns[lockedCol]:
                        if puzz.index(dex).block != key and n in puzz.index(dex).poss:
                            puzz.cells[dex[0]][dex[1]].poss.remove(n)
                            info[1] = "Column"
                            done.append(dex)
                    if len(done) > 0:
                        info[2] = done
                        hist = history(info[0], holder, info[2], n, info[1])
                        return [True, hist]

    return [False]
# Looks for instances where numbers occuring in a row or column all exist in the same block, allowing the elimination of those numbers in the remainder of the block
def lockedCandidate(puzz):
    info = searchLockedCandidate(puzz.rows, puzz)
    if info[0]:
        hist = history("Locked Candidate", info[1], info[2], info[3], "Row")
        return [True, hist]
    info = searchLockedCandidate(puzz.columns, puzz)
    if info[0]:
        hist = history("Locked Candidate", info[1], info[2], info[3], "Column")
        return [True, hist]
    return [False]
# Logic for locked candidates
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
                        puzz.cells[dex[0]][dex[1]].entryButton.background_color = (0, 0, 1, 1)
                        updated.append(dex)
                if len(updated) > 0:
                    for dex in found:
                        puzz.cells[dex[0]][dex[1]].entryButton.background_color = (1, 0, 0, 1)
                    return [True, check, updated, n]
    return [False]
# Checks rows, columns, and blocks for pairs of cells that share the same ONLY TWO possibilities, removes those possibilities from other related cells
def nakedPairs(puzz):
    check = searchNakedPairs(puzz.rows, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Naked Pair", check[1], check[3], check[2], "Row")
        return [True, info]
    check = searchNakedPairs(puzz.columns, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Naked Pair", check[1], check[3], check[2], "Column")
        return [True, info]
    check = searchNakedPairs(puzz.blocks, puzz)  
    if not check[0]:
        pass
    else: 
        info = history("Naked Pair", check[1], check[3], check[2], "Block")
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
            updated = updateNakedPair(found, puzz)
            if updated[0]:
                return [True, found, puzz.index(found[0]).poss, updated[1]]
        maybes.clear()
    return [False]
# Compares a list of cells, returns indexes if a pair is found
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
                        puzz.cells[dex[0]][dex[1]].entryButton.background_color = (0, 0, 1, 1)
                        updated.append(dex)
    # Otherwise if the pair occurred in a column, clear related cells from the column
    elif cell1[1] == cell2[1]:
        for dex in puzz.columns[cell1[1]]:
            if dex != cell1 and dex != cell2:
                for i in range(2):
                    if pairValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(pairValues[i])
                        puzz.cells[dex[0]][dex[1]].entryButton.background_color = (0, 0, 1, 1)
                        updated.append(dex)
    # Pairs from rows or columns can also share a block, so always checks the blocks for pairs
    if puzz.index(cell1).block == puzz.index(cell2).block:
        for dex in puzz.blockDic[puzz.index(cell1).block]:
            if dex != cell1 and dex != cell2:
                for i in range(2):
                    if pairValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(pairValues[i])
                        puzz.cells[dex[0]][dex[1]].entryButton.background_color = (0, 0, 1, 1)
                        updated.append(dex)
    if len(updated) > 0:
        return [True, updated]
    else:
        return [False]
# Runs through rows, columns, and blocks, returns information on the found pair
def hiddenPairs(puzz):
    check = searchHiddenPairs(puzz.rows, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Hidden Pair", check[1], [], check[2], "Row")
        return [True, info]
    check = searchHiddenPairs(puzz.columns, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Hidden Pair", check[1], [], check[2], "Column")
        return [True, info]
    check = searchHiddenPairs(puzz.blocks, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Hidden Pair", check[1], [], check[2], "Block")
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
                        removed = []
                        if puzz.cells[pairs[i][0][0]][pairs[i][0][1]].updateHidden(found):
                            removed.append(pairs[i][0])
                        if puzz.cells[pairs[i][1][0]][pairs[i][1][1]].updateHidden(found):
                            removed.append(pairs[i][1])
                        if len(removed) > 0:
                            return [True, removed, found]
        # Re-initialize starting values
        maybes.clear()
        pairs.clear()
        for key in puzz.nums:
            numCount[key] = 0
    return [False]
# Runs through rows, columns, and blocks, returns information on any found triple
def nakedTriples(puzz):
    check = searchNakedTriples(puzz.rows, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Naked Triple", check[1], check[2], check[3], "Row")
        return [True, info]
    check = searchNakedTriples(puzz.columns, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Naked Triple", check[1], check[2], check[3], "Column")
        return [True, info]
    check = searchNakedTriples(puzz.blocks, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Naked Triple", check[1], check[2], check[3], "Block")
        return [True, info]
    return [False]
# Checks for cells with only two or three possibilities, passes those cells to the search function
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
            check = updateNakedTriple(found, puzz)
            if check[0]:
                return [True, found, check[1], puzz.index(found[0]).poss]
        maybes.clear()
    return [False]
# Compares a given list of cells and checks for instances where three cells share a pool of three possible answers
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
# Removes the triple values from related cells
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
                        puzz.cells[dex[0]][dex[1]].entryButton.background_color = (0, 0, 1, 1)
                        updated.append(dex)
    # Otherwise if the triple occurred in a column, clear related cells from the column
    elif cells[0][1] == cells[1][1] and cells[1][1] == cells[2][1]:
        for dex in puzz.columns[cells[0][1]]:
            if dex != cells[0] and dex != cells[1] and dex != cells[2]:
                for i in range(3):
                    if tripValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(tripValues[i])
                        puzz.cells[dex[0]][dex[1]].entryButton.background_color = (0, 0, 1, 1)
                        updated.append(dex)
    # Triples from rows or columns can also share a block, so always checks the blocks for triples
    if puzz.index(cells[0]).block == puzz.index(cells[1]).block and puzz.index(cells[1]).block == puzz.index(cells[2]).block:
        for dex in puzz.blockDic[puzz.index(cells[0]).block]:
            if dex != cells[0] and dex != cells[1] and dex != cells[2]:
                for i in range(3):
                    if tripValues[i] in puzz.cells[dex[0]][dex[1]].poss:
                        puzz.cells[dex[0]][dex[1]].poss.remove(tripValues[i])
                        puzz.cells[dex[0]][dex[1]].entryButton.background_color = (0, 0, 1, 1)
                        updated.append(dex)
    if len(updated) > 0:
        for cause in trip:
            puzz.cells[cause[0]][cause[1]].entryButton.backgroundColor = (1, 0, 0, 1)
        return [True, updated]
    else:
        return [False]
# Runs through rows, columns, and blocks for instances of hidden triples, returns some data
def hiddenTriples(puzz):
    check = searchHiddenTriples(puzz.rows, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Hidden Triple", check[1], [], check[2], "Row")
        return [True, info]
    check = searchHiddenTriples(puzz.columns, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Hidden Triple", check[1], [], check[2], "Column")
        return [True, info]
    check = searchHiddenTriples(puzz.blocks, puzz)
    if not check[0]:
        pass
    else: 
        info = history("Hidden Triple", check[1], [], check[2], "Block")
        return [True, info]
    return [False]
# Checks for instances where in a given group of cells, a set of three numbers occurs only in three cells
def searchHiddenTriples(category, puzz):
    numCount = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}
    maybes = []
    trips = []
    found = None
    # Checks rows for hidden triples
    for group in category:
        # Count up how many times each number is possible
        for n in puzz.nums:
            for i in range(9):
                if n in puzz.index(group[i]).poss:
                    numCount[n] += 1
        # Save the numbers with two or three possible locations
        for n in puzz.nums:
            if 2 <= numCount[n] <= 3:
                maybes.append(n)
        # Put indexes of potential triple cells in an array, with number value
        if len(maybes) > 1:
            trips = []
            for n in maybes:
                trip = []
                for i in range(9):
                    if n in puzz.index(group[i]).poss:
                        trip.append(group[i])
                trip.append(n)
                trips.append(trip)
        # Check if any of the triples match
        if len(trips) > 2:
            for i in range(len(trips) - 1):
                for j in range(i + 1, len(trips)):
                    for k in range(j + 1, len(trips)):
                        indexes = [trips[i][:-1], trips[j][:-1], trips[k][:-1]]
                        unique = []
                        for trip in indexes:
                            for index in trip:
                                if index not in unique:
                                    unique.append(index)
                        if len(unique) == 3:
                            found = [trips[i][-1], trips[j][-1], trips[k][-1]]
                            removed = []
                            for dex in unique:
                                if puzz.cells[dex[0]][dex[1]].updateHidden(found):
                                    removed.append(dex)
                            if len(removed) > 0:
                                return [True, removed, found]
        # Re-initialize starting values
        maybes.clear()
        trips.clear()
        for key in puzz.nums:
            numCount[key] = 0
    return [False]

def Xwing(puzz):
    check = searchXwing(puzz.rows, puzz, "r")
    if check[0]:
        hist = history("X wing", check[1], check[2], check[3], "Row")
        return [True, hist]
    check = searchXwing(puzz.columns, puzz, "c")
    if check[0]:
        hist = history("X wing", check[1], check[2], check[3], "Column")
        return [True, hist]
    return [False]

def searchXwing(category, puzz, cat):
    found = []
    for n in puzz.nums:
        # Saves every instance of number n being possible only twice in either rows or columns
        pairs = []
        for group in category:
            numCount = 0
            holder = []
            for dex in group:
                if n in puzz.index(dex).poss:
                    numCount += 1
                    holder.append(dex)
            if numCount == 2:
                pairs.append(holder)
        # Compare found pairs. If rows were checked, check that the columns also match, if columns were checked, check that the rows also match
        if cat == "r":
            for i in range(len(pairs) - 1):
                for j in range(i + 1, len(pairs)):
                    if pairs[i][0][1] == pairs[j][0][1] and pairs[i][1][1] == pairs[j][1][1]:
                        for row in range(9):
                            if row == pairs[i][0][0] or row == pairs[j][0][0]:
                                pass
                            else:
                                if n in puzz.cells[row][pairs[i][0][1]].poss:
                                    puzz.cells[row][pairs[i][0][1]].poss.remove(n)
                                    puzz.cells[row][pairs[i][0][1]].entryButton.background_color = (0, 0, 1, 1)
                                    found.append((row, pairs[i][0][1]))
                                if n in puzz.cells[row][pairs[i][1][1]].poss:
                                    puzz.cells[row][pairs[i][1][1]].poss.remove(n)
                                    puzz.cells[row][pairs[i][1][1]].entryButton.background_color = (0, 0, 1, 1)
                                    found.append((row, pairs[i][1][1]))
                        if len(found) > 0:
                            return [True, [pairs[i][0], pairs[i][1], pairs[j][0], pairs[j][1]], found, n]
        elif cat == "c":
            for i in range(len(pairs) - 1):
                for j in range(i + 1, len(pairs)):
                    if pairs[i][0][0] == pairs[j][0][0] and pairs[i][1][0] == pairs[j][1][0]:
                        for col in range(9):
                            if col == pairs[i][0][1] or col == pairs[j][0][1]:
                                pass
                            else:
                                if n in puzz.cells[pairs[i][0][0]][col].poss:
                                    puzz.cells[pairs[i][0][0]][col].poss.remove(n)
                                    puzz.cells[pairs[i][0][0]][col].entryButton.background_color = (0, 0, 1, 1)
                                    found.append((pairs[i][0][0], col))
                                if n in puzz.cells[pairs[i][1][0]][col].poss:
                                    puzz.cells[pairs[i][1][0]][col].poss.remove(n)
                                    puzz.cells[pairs[i][1][0]][col].entryButton.background_color = (0, 0, 1, 1)
                                    found.append((pairs[i][1][0], col))
                        if len(found) > 0:
                            return [True, [pairs[i][0], pairs[i][1], pairs[j][0], pairs[j][1]], found, n]
    return [False]

def Ywing(puzz):
    maybes = []
    removed = []
    for rx in range(9):
        for cx in range(9):
            cellX = cellY = cellZ = possA = possB = possC = None
            if len(puzz.cells[rx][cx].poss) == 2:
                possA = puzz.index((rx, cx)).poss[0]
                possB = puzz.index((rx, cx)).poss[1]
                cellX = (rx, cx)
                for ry in range(9):
                    for cy in range(9):
                        if puzz.index(cellX).sees((ry, cy), puzz) and len(puzz.index((ry, cy)).poss) == 2 and puzz.index(cellX).poss != puzz.index((ry, cy)).poss:
                            if possA in puzz.index((ry, cy)).poss or possB in puzz.index((ry, cy)).poss:
                                maybes.append(puzz.index((ry, cy)))
                if len(maybes) > 1:
                    Ys = checkYwing(puzz.index(cellX), maybes)
                    if Ys != False:
                        for found in Ys:
                            cellY, cellZ, possC = found[0], found[1], found[2]
                            for rz in range(9):
                                for cz in range(9):
                                    if puzz.index((rz, cz)).sees(cellY, puzz) and puzz.index((rz, cz)).sees(cellZ, puzz):
                                        if possC in puzz.index((rz, cz)).poss:
                                            puzz.cells[rz][cz].poss.remove(possC)
                                            puzz.cells[rz][cz].entryButton.background_color = (0, 0, 1, 1)
                                            puzz.cells[cellX[0]][cellX[1]].entryButton.background_color = (1, 1, 0, 1)
                                            puzz.cells[cellY[0]][cellY[1]].entryButton.background_color = (1, 0, 0, 1)
                                            puzz.cells[cellZ[0]][cellZ[1]].entryButton.background_color = (1, 0, 0, 1)
                                            removed.append((rz, cz))
                            if len(removed) > 0:
                                hist = history("Y wing", [cellX, cellY, cellZ], removed, possC, "Cell")
                                return [True, hist]
                maybes.clear()
    return [False]

def checkYwing(cellX, maybes):
    possA, possB = cellX.poss[0], cellX.poss[1]
    possC = None
    Ys = []
    for i in range(len(maybes) - 1):
        for nY in maybes[i].poss:
            if nY != possA and nY != possB:
                possC = nY
                for j in range(i + 1, len(maybes)):
                    if possC in maybes[j].poss and maybes[i].poss != maybes[j].poss:
                        Ys.append([maybes[i].index, maybes[j].index, possC])
    if len(Ys) > 0:
        return Ys
    return False

def simpleColoring(puzz):
    for n in puzz.nums:
        chains = findChains(n, puzz)
        if chains != False:
            info = history("Simple Coloring", chains[1], chains[0], chains[2], chains[3])
            return [True, info]
        
    return [False]

def findChains(n, puzz):
    # by number, search for chains of strong connections
    chains = []
    colors = ("r", "b")
    chainCount = 0
    # A dictionary of dictionaries using cell indexes as keys to the dictionaries storing the cells chain data.
    cellInfo = {}
    # Populates cellInfo dictionary
    for i in range(9):
        for j in range(9):
            cellInfo[(i, j)] = {'chained': False, 'color': None, 'chain': 0}
    
    for group in puzz.rows:
        for dex in group:
            if n in puzz.index(dex).poss:
                if not cellInfo[dex]['chained']:
                    oneChain = []
                    chainHolder = findDependants(dex, n, puzz, oneChain)
                    if chainHolder != False:
                        if len(chainHolder) > 2:
                            for link in chainHolder:
                                cellInfo[link]['chained'] = True
                            chains.append(chainHolder)
    # Color the first cell in the list "r", then loop through all the cells in the list, if they see each other mark them as the alternate color.
    if len(chains) == 0:
        return False
    for linked in chains:
        chainCount += 1
        cellInfo[linked[0]]['color'] = 'r'
        cellInfo[linked[0]]['chain'] = chainCount
        for linkA in range(0, len(linked) - 1):
            for linkB in range(linkA + 1, len(linked)):
                if puzz.index(linked[linkA]).dependsOn(linked[linkB], n, puzz):
                    if cellInfo[linked[linkA]]['color'] == 'r' and cellInfo[linked[linkB]]['chain'] == 0:
                        cellInfo[linked[linkB]]['color'] = 'b'
                        cellInfo[linked[linkB]]['chain'] = chainCount
                    elif cellInfo[linked[linkA]]['color'] == 'b' and cellInfo[linked[linkB]]['chain'] == 0:
                        cellInfo[linked[linkB]]['color'] = 'r'
                        cellInfo[linked[linkB]]['chain'] = chainCount
                        # POTENTIAL PROBLEM: if the cells in the list are not arranged in the order of the chain, this will iterate to cells that have no color as linkA, breaking the coloring chain.
                        # However, we make the chain recursively so it should be in order.
    # First make sure it's a valid chain

    for chain in chains:
        invalid = []
        for cellN in chain:
            color = None
            for checkcellN in chain:
                if puzz.index(cellN).sees(checkcellN, puzz):
                    if cellInfo[checkcellN]['color'] == cellInfo[cellN]['color']:
                        color = cellInfo[cellN]['color']
                        for bad in chain:
                            if cellInfo[bad]['color'] == color:
                                invalid.append(bad)
                        if len(invalid) > 0:
                            for badboy in invalid:
                                if n in puzz.index(badboy).poss:
                                    puzz.index(badboy).poss.remove(n)
                            return [invalid, chain, n, "Invalid chain"]
                   # Correctly identifies invalid chains, incorrectly removes possibilities 

    for chain in chains:
        found = []
        for group in puzz.rows:
            for cell in group:
                colors = []
                if n in puzz.index(cell).poss and cell not in chain:
                    for checkCell in chain:
                        if puzz.index(cell).sees(checkCell, puzz):
                            colors.append(cellInfo[checkCell]['color'])
                    if len(colors) > 1:
                        unique = []
                        for color in colors:
                            if color not in unique:
                                unique.append(color)
                        if len(unique) > 1:
                            found.append(cell)
        if len(found) > 0:
            for badDex in found:
                puzz.cells[badDex[0]][badDex[1]].poss.remove(n)
            return [found, chain, n, "Multi color"]
    return False

def findDependants(dex, n, puzz, lst):
    Dlist = lst
    count = 0
    holder = []
    tmp = []
    # base case
    if dex in Dlist:
        return
    else:
        Dlist.append(dex)
    # Checks related row, column, and block for instances where there is only one other possible cell with the same value
    for i in range(9):
        if i != dex[0]:
            if n in puzz.cells[i][dex[1]].poss:
                count += 1
                tmp.append((i, dex[1]))
    if count == 1:
        holder.append(tmp[0])
    tmp.clear()
    count = 0
    for i in range(9):
        if i != dex[1]:
            if n in puzz.cells[dex[0]][i].poss:
                count += 1
                tmp.append((dex[0], i))
    if count == 1:
        holder.append(tmp[0])
    tmp.clear()
    count = 0
    for blockMate in puzz.blockDic[puzz.index(dex).block]:
        if blockMate != dex:
            if n in puzz.index(blockMate).poss:
                count += 1
                if blockMate[0] != dex[0] and blockMate[1] != dex[1]:
                    tmp.append((blockMate))
    if count == 1 and len(tmp) == 1:
        holder.append(tmp[0])
    tmp.clear()
    count = 0
    if len(holder) == 0:
        return False
    for dependant in holder:
        if dependant not in Dlist:
            findDependants(dependant, n, puzz, Dlist)
    return Dlist