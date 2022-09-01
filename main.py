from kivy.config import Config

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '800')

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.clock import Clock
from methods import *


sudoku_toggles = []
selection_buttons = []
puzz = puzzle()
step = 0
pressedButton = ToggleButton
solveHistory = []
Complete = False
SolveSpeed = .05

easyExample = (6, 8, 0, 0, 0, 0, 0, 1, 7,
                0, 0, 5, 0, 0, 3, 0, 0, 0,
                0, 0, 0, 0, 7, 0, 6, 5, 0,
                0, 0, 0, 4, 3, 0, 0, 0, 8,
                3, 9, 8, 7, 2, 0, 4, 6, 0,
                0, 6, 7, 5, 9, 0, 1, 2, 3,
                5, 3, 0, 0, 0, 7, 2, 0, 0,
                0, 0, 0, 0, 6, 0, 0, 0, 1,
                0, 4, 6, 0, 8, 2, 0, 0, 0)

mediumExample = (4, 8, 0, 0, 0, 0, 5, 0, 0,
                0, 0, 0, 5, 4, 8, 3, 9, 7,
                0, 0, 0, 0, 0, 0, 8, 0, 0,
                0, 0, 4, 1, 8, 0, 2, 3, 0,
                0, 0, 8, 0, 0, 6, 0, 0, 0,
                0, 5, 0, 0, 7, 3, 0, 0, 8,
                0, 7, 2, 3, 0, 9, 0, 0, 0,
                0, 0, 3, 0, 0, 0, 0, 2, 5,
                0, 0, 0, 0, 6, 2, 9, 0, 3)

hardExample = (0, 0, 0, 0, 6, 0, 4, 2, 0,
                5, 0, 0, 0, 0, 7, 0, 8, 0, 
                0, 0, 7, 0, 0, 0, 0, 0, 0, 
                6, 1, 0, 0, 0, 0, 5, 0, 0, 
                0, 0, 0, 0, 8, 0, 0, 3, 0, 
                0, 5, 8, 0, 0, 9, 0, 0, 0,
                4, 0, 0, 0, 2, 0, 0, 0, 0,
                0, 0, 1, 4, 0, 0, 0, 0, 6,
                2, 0, 6, 0, 0, 0, 0, 0, 9)

expertExample = (0, 9, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 1, 9, 0, 3, 0, 7,
                0, 0, 0, 8, 0, 0, 0, 0, 0,
                0, 0, 5, 0, 7, 0, 0, 0, 9,
                0, 0, 0, 4, 0, 0, 0, 8, 1,
                0, 2, 0, 0, 0, 0, 0, 7, 0,
                0, 7, 0, 0, 0, 4, 0, 0, 0,
                0, 0, 0, 2, 5, 0, 0, 4, 0,
                5, 0, 9, 0, 0, 3, 0, 2, 0)

evilExample = (0, 0, 0, 6, 0, 0, 0, 8, 0,
                0, 4, 0, 0, 0, 0, 0, 2, 0,
                5, 0, 0, 0, 9, 0, 4, 0, 6,
                0, 5, 0, 2, 0, 0, 7, 0, 1,
                9, 0, 0, 0, 0, 3, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 4, 0,
                0, 0, 1, 0, 2, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 8,
                0, 7, 0, 1, 0, 0, 6, 0, 5)


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.Message = "Enter your puzzle"
        self.gameState = "Entry"
        self.ids.historySlider.bind(value = self.displayHistory)
    # Makes sure only one cell is selected at a time
    def switch_active(self, togglebutton):
        global pressedButton
        tb = togglebutton
        for i in range(9):
            for j in range(9):
                if tb == puzz.cells[i][j].entryButton:
                    cellCount = 0
                    cellCount += 1
                    self.ids.cellData.text = f"Cell possibilities: \n {puzz.cells[i][j].poss}, Block: {puzz.cells[i][j].block}, Index: {puzz.cells[i][j].index}"
                else:
                    puzz.cells[i][j].entryButton.state = "normal"
        if tb.state == "down":
            for number in selection_buttons:
                number.disabled = False
        else:
            for number in selection_buttons:
                number.disabled = True

    # Commits filled in puzzle to cell array
    def fill_example(self, button):
        position = 0
        if button.text == "E":
            for i in range(9):
                for j in range(9):
                    if easyExample[position] > 0:
                        puzz.cells[i][j].entryButton.text = str(easyExample[position])
                    else:
                        puzz.cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "M":
            for i in range(9):
                for j in range(9):
                    if mediumExample[position] > 0:
                        puzz.cells[i][j].entryButton.text = str(mediumExample[position])
                    else:
                        puzz.cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "H":
            for i in range(9):
                for j in range(9):
                    if hardExample[position] > 0:
                        puzz.cells[i][j].entryButton.text = str(hardExample[position])
                    else:
                        puzz.cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "X":
            for i in range(9):
                for j in range(9):
                    if expertExample[position] > 0:
                        puzz.cells[i][j].entryButton.text = str(expertExample[position])
                    else:
                        puzz.cells[i][j].entryButton.text = ""
                    position += 1

    def run_solver(self, button):
        global step
        if button.text == "Lock in puzzle":
            for i in range(9):
                for j in range(9):
                    if puzz.cells[i][j].entryButton.text != "":
                        puzz.cells[i][j].value = puzz.cells[i][j].entryButton.text
                        puzz.cells[i][j].entryButton.color = [0, 0, 0, 1]
                        puzz.cells[i][j].poss.clear()
                        puzz.cells[i][j].updateRelated(puzz)
            button.text = "Get Hint"
            self.gameState = "Hints"
            self.ids.entryGrid.pos_hint = {'right': 0}
            self.ids.possDisplay.pos_hint = {'right': .75}
        else:
            move = findNextMove(puzz)
            if move[0]:
                solveHistory.append(move[1].record)
                print(move[1].record)
                self.colorCells(move[1].record, puzz)
                self.ids.historySlider.max = step
                self.ids.historySlider.value = step
                step += 1    

    def displayHistory(self, slider, value):
        self.ids.historyDisplay.text = f"Found {solveHistory[int(value)]['method']} at: {solveHistory[int(value)]['cause']}"
        if self.ids.historySlider.value < step:
            #erase filled cells up to the point of the value
            pass
        self.colorCells(solveHistory[int(value)], puzz)

    def colorCells(self, hist, puzz):
        move = hist['method']
        loc = hist['cause']
        if move == "Fill In":
            puzz.colorOnly([loc], [1, 1, 1, 1])
        elif move == "Naked Single":
            puzz.colorOnly([loc], [0, 1, 0, 1])
        elif move == "Hidden Single":
            puzz.colorOnly([loc], [0, 1, 0, 1])
        elif move == "Pointer":
            pass
        elif move == "Locked Candidate":
            pass
        elif move == "Naked Pair":
            pass
        elif move == "Hidden Pair":
            puzz.colorOnly(loc, [0, 0, 1, 1])
        elif move == "Naked Triple":
            pass
        elif move == "Hidden Triple":
            puzz.colorOnly(loc, [0, 0, 1, 1])
        elif move == "X wing":
            pass
        elif move == "Y wing":
            pass
        elif move == "Simple Coloring":
            pass
        

    def reset(self, button):
        global puzz
        puzz = puzzle()
        count = 0
        self.ids.startButton.text = "Lock in puzzle"
        self.ids.entryGrid.pos_hint = {'right': .75}
        self.ids.possDisplay.pos_hint = {'right': 0}
        for i in range(9):
            for j in range(9):
                puzz.cells[i][j] = cell(i, j, sudoku_toggles[count])
                puzz.cells[i][j].entryButton.text = ""
                puzz.cells[i][j].entryButton.background_color = (1, 1, 1, 1)
                puzz.cells[i][j].entryButton.color = [1, 1, 1, 1]
                puzz.cells[i][j].entryButton.state = "normal"
                count += 1

    def solveAll(self, button):
            Clock.schedule_interval(self.next, SolveSpeed)
    
    def next(self, dt):
        global step
        global Complete
        move = findNextMove(puzz)
        if move[0]:
            solveHistory.append(move[1].record)
            self.ids.historySlider.max = step
            self.ids.historySlider.value = step
            self.ids.historyDisplay.text = f"Found {solveHistory[step]['method']} at: {solveHistory[step]['cause']}"
            step += 1
            return True
        else:
            Complete = True
            return False


class SudokuButtons(GridLayout):
    # Creates cells and fills cell array
    def __init__(self, **kwargs):
        super(SudokuButtons, self).__init__(**kwargs)
        spaceWidth = 3
        for i in range(9):
            rowSpacer = Label(size_hint = (0, None), height = spaceWidth)
            for j in range(3):
                columnSpacer = Label(size_hint = (None, 0), width = spaceWidth)
                for k in range(3):
                    b = ToggleButton()
                    sudoku_toggles.append(b)
                    self.add_widget(b)
                self.add_widget(columnSpacer)
            if (i + 1) % 3 == 0:
                for a in range(12):
                    rowSpacer = Label(size_hint = (0, None), height = spaceWidth)
                    self.add_widget(rowSpacer)
        count = 0
        for i in range(9):
            for j in range(9):
                newCell = cell(i, j, sudoku_toggles[count])
                puzz.cells[i][j] = newCell
                count += 1
    
    
class EntryLayout(RelativeLayout):
    def __init__(self,**kwargs):
        super(EntryLayout,self).__init__(**kwargs)
        pass
    # First press updates cells possible values based on entered info.
    # Second and on generates new hints

            


class OptionGrid(GridLayout):
    # Creates option selection buttons
    def __init__(self, **kwargs):
        super(OptionGrid, self).__init__(**kwargs)
        for i in range(0, 10):
            title = ""
            if i > 0:
                title = str(i)
            b = Button(text=title, disabled = True, on_press = self.num_entry)
            selection_buttons.append(b)
            self.add_widget(b)
    # Enters writes option to selected cell
    def num_entry(self, button):
        for c in sudoku_toggles:
            if c.state == "down":
                c.text = button.text
                c.state = "normal"
                for butt in selection_buttons:
                    butt.disabled = True
                return
        for butt in selection_buttons:
            butt.disabled = True


class SudokuPartnerApp(App):
    def build(self):
        return MainScreen()


SudokuPartnerApp().run()