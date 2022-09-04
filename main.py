from kivy.config import Config

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '800')

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from methods import *

#TODO erase numbers when scrolling through history, add example puzzles to Help screen, possibly add "possible" numbers to cells, enable keyboard entry of numbers, more rules?

sudoku_toggles = []
selection_buttons = []
puzz = puzzle()
helperPuzz = puzzle()
step = 0
solveHistory = []
Complete = False
SolveSpeed = .03
helper_toggles = []

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


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.Message = "Enter your puzzle"
        self.gameState = "Entry"
        self.ids.historySlider.bind(value = self.displayHistory)
    # Makes sure only one cell is selected at a time
    def switch_active(self, togglebutton):
        tb = togglebutton
        for i in range(9):
            for j in range(9):
                if tb == puzz.cells[i][j].entryButton:
                    cellCount = 0
                    cellCount += 1
                    self.ids.cellData.text = f"Cell possibilities: \n {puzz.cells[i][j].poss}"
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
        global Complete
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
                self.addHistory()
                print(move[1].record)
                self.colorCells(move[1].record, puzz)
                self.ids.historySlider.disabled = False
                self.ids.historySlider.max = step
                self.ids.historySlider.value = step
                step += 1
            else:
                Complete = True

    def addHistory(self):
        message = solveHistory[step]['method']
        newLabel = HistoryLabel(text = message)
        newLabel.stepCount = step
        self.ids.historyDisplay.add_widget(newLabel) 
    
    def displayHistory(self, slider, value):
        # Move historyDisplay to match the value of the slider
        self.ids.historyDisplay.pos_hint['top'] = (int(value) + 2.5) * .2
        self.ids.scrollHolder.do_layout()
        for each in self.ids.historyDisplay.children:
            each.updateOpacity(int(value))
        # If we don't call the "do layout" method, the new position of the hsitoryDisplay layout isn't updated until the screen is resized.
        self.colorCells(solveHistory[int(value)], puzz)

    def colorCells(self, hist, puzz):
        move = hist['method']
        cause = hist['cause']
        effect = hist['effect']
        num = hist['number']
        category = hist['category']
        if move == "Fill In":
            puzz.colorIn(([cause], [1, 1, 1, 1]))
        elif move == "Naked Single":
            puzz.colorIn(([cause], [0, 1, 0, 1]))
        elif move == "Hidden Single":
            puzz.colorIn(([cause], [0, 1, 0, 1]))
        elif move == "Pointer":
            puzz.colorIn((cause, [0, 0, 1, 1]), (effect, [1, 1, 0, 1]))
        elif move == "Locked Candidate":
            puzz.colorIn((cause, [0, 0, 1, 1]), (effect, [1, 1, 0, 1]))
        elif move == "Naked Pair":
            puzz.colorIn((cause, [0, 0, 1, 1]), (effect, [1, 1, 0, 1]))
        elif move == "Hidden Pair":
            puzz.colorIn((cause, [0, 0, 1, 1]))
        elif move == "Naked Triple":
            puzz.colorIn((cause, [0, 0, 1, 1]), (effect, [1, 1, 0, 1]))
        elif move == "Hidden Triple":
            puzz.colorIn((cause, [0, 0, 1, 1]))
        elif move == "X wing":
            puzz.colorIn((cause, [0, 0, 1, 1]), (effect, [1, 1, 0, 1]))
        elif move == "Y wing":
            puzz.colorIn((cause, [0, 0, 1, 1]), (effect, [1, 1, 0, 1]))
        elif move == "Simple Coloring":
            puzz.colorIn((cause, [0, 0, 1, 1]), (effect, [1, 1, 0, 1]))

    def reset(self, button):
        global puzz
        global step
        puzz = puzzle()
        count = 0
        self.ids.startButton.text = "Lock in puzzle"
        self.ids.entryGrid.pos_hint = {'right': .75}
        self.ids.possDisplay.pos_hint = {'right': 0}
        self.ids.historyDisplay.text = ""
        step = 0
        self.ids.historySlider.disabled = True
        self.ids.historyDisplay.clear_widgets()
        solveHistory.clear()
        for i in range(9):
            for j in range(9):
                puzz.cells[i][j] = cell(i, j, sudoku_toggles[count])
                puzz.cells[i][j].entryButton.text = ""
                puzz.cells[i][j].entryButton.background_color = (1, 1, 1, 1)
                puzz.cells[i][j].entryButton.color = [1, 1, 1, 1]
                puzz.cells[i][j].entryButton.state = "normal"
                count += 1

    def solveAll(self, button):
        self.ids.historySlider.disabled = False
        Clock.schedule_interval(self.next, SolveSpeed)
    
    def next(self, dt):
        global step
        global Complete
        move = findNextMove(puzz)
        if move[0]:
            solveHistory.append(move[1].record)
            self.ids.historySlider.max = step
            self.ids.historySlider.value = step
            self.addHistory()
            step += 1
            return True
        else:
            Complete = True
            return False

class HelperSudoku(GridLayout):
    def __init__(self, **kwargs):
        super(HelperSudoku, self).__init__(**kwargs)
        spaceWidth = 3
        for i in range(9):
            rowSpacer = Label(size_hint = (0, None), height = spaceWidth)
            for j in range(3):
                columnSpacer = Label(size_hint = (None, 0), width = spaceWidth)
                for k in range(3):
                    b = ToggleButton()
                    helper_toggles.append(b)
                    self.add_widget(b)
                if j < 2:
                    self.add_widget(columnSpacer)
            if (i + 1) % 3 == 0:
                for a in range(11):
                    rowSpacer = Label(size_hint = (0, None), height = spaceWidth)
                    self.add_widget(rowSpacer)
        count = 0
        for i in range(9):
            for j in range(9):
                newCell = cell(i, j, helper_toggles[count])
                helperPuzz.cells[i][j] = newCell
                count += 1

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
                if j < 2:
                    self.add_widget(columnSpacer)
            if (i + 1) % 3 == 0:
                for a in range(11):
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
        
    # First press updates cells possible values based on entered info.
    # Second and on generates new hints

class HistoryScroll(StackLayout):
    def __init__(self,**kwargs):
        super(HistoryScroll,self).__init__(**kwargs)
        

class HistoryLabel(Label):
    def __init__(self,**kwargs):
        super(HistoryLabel,self).__init__(**kwargs)
        self.stepCount = None

    def updateOpacity(self, stepN):
        opacity = 1
        background = (1, 1, 1, .3)
        diff = stepN - self.stepCount
        if 0 < diff < 5:
            opacity = 1 - diff / 4
            background = (1, 1, 1, 0)
        elif 0 > diff > -3:
            opacity = 1 - -diff / 2
            background = (1, 1, 1, 0)
        elif diff == 0:
            pass
        else:
            opacity = 0
            background = (1, 1, 1, 0)
        
        self.background_color = background
        self.color = [1, 1, 1, opacity]

class OptionGrid(GridLayout):
    # Creates option selection buttons
    def __init__(self, **kwargs):
        super(OptionGrid, self).__init__(**kwargs)
        for i in range(0, 10):
            title = "Erase"
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

class HelpScreen(Screen):
    def __init__(self, **kwargs):
        super(HelpScreen, self).__init__(**kwargs)
        self.colorExamples = {"Naked Single": ([(0, 4)], [0, 1, 0, 1])}
        self.examplePuzzles = {
            "Naked Single": (1, 2, 3, 4, 0, 6, 7, 8, 9,
                            0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 0, 0, 0)
                            }
    
    def fillHelper(self, rule):
        position = 0
        filler = self.examplePuzzles[rule]
        colorGuide = self.colorExamples[rule]
        for i in range(9):
            for j in range(9):
                if filler[position] > 0:
                    helperPuzz.cells[i][j].entryButton.text = str(filler[position])
                else:
                    helperPuzz.cells[i][j].entryButton.text = ""
                position += 1
        for colorme in colorGuide[0]:
            helperPuzz.cells[colorme[0]][colorme[1]].entryButton.background_color = colorGuide[1]

    def chooseHint(self, value):
        rule = solveHistory[int(value)]['method']
        self.fillHelper(rule)
        explanations = {
            "Naked Single" : "The highlighted cell has only one possible answer.",
            "Hidden Single" : "The highlighted cell is the only cell in its group able to be the given value.",
            "Fill In" : "The cell has been filled, which tells us the other cells that it sees can no longer have the same value.",
            "Pointer": "The value must be in one of the BLUE cells in the block, which means that the value cannot be in any of the related YELLOW cells.",
            "Locked Candidate": "The value cannot appear in any of the RED cells, therefore it must occur in one of the BLUE cells, and can be eliminated from the YELLOW cells.",
            "Naked Pair": "The BLUE cells share a pair of possibilities, meaning one of them must be one of the values, while the other must be the other value. This means these two possibilities can be eliminated from all of the YELLOW cells.",
            "Hidden Pair": "The BLUE cells are the only cells in their group which can possibly be a pair of values. This means all other possibilities can be eliminated from them.",
            "Naked Triple": "The BLUE cells share a trio of possibilities, meaning all of the YELLOW cells cannot contain any of those values.",
            "Hidden Triple": "The BLUE cells are the only cells in their group to have a trio of possibilities, therefore all other possibilities can be eliminated from them.",
            "X wing": "The BLUE cells are the only cells in their rows/columns which can be a certain value. Therefore, all related cells in their row/column cannot be that value.",
            "Y wing": "The BLUE cells share a trio of options in such a way that we know that any cell that can see all three of them cannot have one of those options.",
            "Simple Coloring": "By following a chain of cells that rely on eachother, alternating their color, we can see that there are some cells which will be eliminated whether the chain winds up as blue or red, therefore that value can be eliminated from them."}
        faq = explanations[rule]
        self.ids.explainer.text = faq

class SudokuPartnerApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.main = MainScreen(name = 'mainscreen')
        self.sm.add_widget(self.main)

        self.help = HelpScreen(name = 'helpscreen')
        self.sm.add_widget(self.help)

        return self.sm


SudokuPartnerApp().run()