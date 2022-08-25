from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from methods import *

sudoku_toggles = []
selection_buttons = []
puzz = puzzle()
step = 0
pressedButton = ToggleButton
solveHistory = []

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

hardExample = (0, 0, 0, 0, 0, 0, 6, 0, 0, 
                0, 0, 0, 7, 0, 0, 8, 0, 5,
                0, 0, 1, 0, 2, 8, 0, 3, 0, 
                0, 0, 0, 0, 0, 6, 0, 2, 8,
                0, 0, 2, 1, 5, 0, 9, 0, 0,
                0, 0, 0, 0, 0, 4, 0, 7, 0,
                0, 8, 4, 0, 0, 0, 0, 5, 0, 
                0, 0, 3, 5, 4, 0, 0, 0, 7,
                2, 0, 7, 0, 0, 0, 4, 0, 9)

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
    # Makes sure only one cell is selected at a time
    def switch_active(self, togglebutton):
        global pressedButton
        tb = togglebutton
        count = 0
        for i in range(9):
            for j in range(9):
                if tb == puzz.cells[i][j].entryButton:
                    cellCount = 0
                    cellCount += 1
                    self.ids.myMessage.text = f"Cell possibilities: \n {puzz.cells[i][j].poss}"
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
        if button.text == "Easy example":
            for i in range(9):
                for j in range(9):
                    if easyExample[position] > 0:
                        puzz.cells[i][j].entryButton.text = str(easyExample[position])
                    else:
                        puzz.cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "Medium example":
            for i in range(9):
                for j in range(9):
                    if mediumExample[position] > 0:
                        puzz.cells[i][j].entryButton.text = str(mediumExample[position])
                    else:
                        puzz.cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "Hard example":
            for i in range(9):
                for j in range(9):
                    if hardExample[position] > 0:
                        puzz.cells[i][j].entryButton.text = str(hardExample[position])
                    else:
                        puzz.cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "Evil example":
            for i in range(9):
                for j in range(9):
                    if evilExample[position] > 0:
                        puzz.cells[i][j].entryButton.text = str(evilExample[position])
                    else:
                        puzz.cells[i][j].entryButton.text = ""
                    position += 1

class MiddleBit(RelativeLayout):
    pass

class SudokuButtons(GridLayout):
    # Creates cells and fills cell array
    def __init__(self, **kwargs):
        super(SudokuButtons, self).__init__(**kwargs)
        size = dp(35)
        for i in range(9):
            for j in range(9):
                b = ToggleButton(size_hint = (None, None), size = (size, size))
                sudoku_toggles.append(b)
                self.add_widget(b)
                newCell = cell(i, j, b)
                puzz.cells[i][j] = newCell


class EntryLayout(RelativeLayout):
    def __init__(self,**kwargs):
        super(EntryLayout,self).__init__(**kwargs)
        pass
    # First press updates cells possible values based on entered info.
    # Second and on generates new hints
    def run_solver(self, button):
        global step
        if button.text == "Get hint":
            for i in range(9):
                for j in range(9):
                    if puzz.cells[i][j].entryButton.text != "":
                        puzz.cells[i][j].value = puzz.cells[i][j].entryButton.text
                        puzz.cells[i][j].poss.clear()
                        puzz.cells[i][j].updateRelated(puzz)
            button.text = "Next Hint"
        else:
            print(findNextMove(puzz))
    
    def reset(self, button):
        global puzz
        puzz = puzzle()
        count = 81
        self.ids.startButton.text = "Get hint"
        for i in range(9):
            for j in range(9):
                puzz.cells[i][j] = cell(i, j, sudoku_toggles[count])
                puzz.cells[i][j].entryButton.text = ""
                puzz.cells[i][j].entryButton.background_color = (1, 1, 1, 1)
                puzz.cells[i][j].entryButton.state = "normal"
                count += 1


class OptionGrid(GridLayout):
    # Creates option selection buttons
    def __init__(self, **kwargs):
        super(OptionGrid, self).__init__(**kwargs)
        for i in range(0, 10):
            size = dp(35)
            title = ""
            if i > 0:
                title = str(i)
            b = Button(text=title, size_hint=(None, None), size=(size, size), disabled = True, on_press = self.num_entry)
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

class history():
    # A dictionary that keeps a record of each move
    def __init__(self, step, method, index):
        record = {"step": step, "method": method, "index": index}

    
class SudokuPartnerApp(App):
    def build(self):
        return MainScreen()


SudokuPartnerApp().run()