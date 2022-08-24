from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import StringProperty
from methods import *

sudoku_toggles = []
selection_buttons = []
cells = [[None for i in range(9)] for j in range(9)]
blocks = {"tl": [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)], "tm": [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)], "tr": [(0,6),(0,7),(0,8),(1,6),(1,7),(1,8),(2,6),(2,7),(2,8)],
            "ml": [(3,0),(3,1),(3,2),(4,0),(4,1),(4,2),(5,0),(5,1),(5,2)], "mm": [(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)], "mr": [(3,6),(3,7),(3,8),(4,6),(4,7),(4,8),(5,6),(5,7),(5,8)],
            "bl": [(6,0),(6,1),(6,2),(7,0),(7,1),(7,2),(8,0),(8,1),(8,2)], "bm": [(6,3),(6,4),(6,5),(7,3),(7,4),(7,5),(8,3),(8,4),(8,5)], "br": [(6,6),(6,7),(6,8),(7,6),(7,7),(7,8),(8,6),(8,7),(8,8)]}
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
    # Makes sure only one cell is selected at a time
    def switch_active(self, togglebutton):
        global pressedButton
        tb = togglebutton
        for button in sudoku_toggles:
            if tb == button:
                pass
            else:
                button.state = "normal"
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
                        cells[i][j].entryButton.text = str(easyExample[position])
                    else:
                        cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "Medium example":
            for i in range(9):
                for j in range(9):
                    if mediumExample[position] > 0:
                        cells[i][j].entryButton.text = str(mediumExample[position])
                    else:
                        cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "Hard example":
            for i in range(9):
                for j in range(9):
                    if hardExample[position] > 0:
                        cells[i][j].entryButton.text = str(hardExample[position])
                    else:
                        cells[i][j].entryButton.text = ""
                    position += 1
        elif button.text == "Evil example":
            for i in range(9):
                for j in range(9):
                    if evilExample[position] > 0:
                        cells[i][j].entryButton.text = str(evilExample[position])
                    else:
                        cells[i][j].entryButton.text = ""
                    position += 1
    

class SudokuButtons(GridLayout):
    # Creates cells and fills cell array
    def __init__(self, **kwargs):
        super(SudokuButtons, self).__init__(**kwargs)
        for i in range(9):
            for j in range(9):
                size = dp(35)
                b = ToggleButton(size_hint = (None, None), size = (size, size))
                sudoku_toggles.append(b)
                self.add_widget(b)
                newCell = cell(i, j, b)
                cells[i][j] = newCell
                pass


class EntryLayout(RelativeLayout):
    # First press updates cells possible values based on entered info.
    # Second and on generates new hints
    def run_solver(self, button):
        global step
        if button.text == "Get hint":
            for i in range(9):
                for j in range(9):
                    if cells[i][j].entryButton.text != "":
                        cells[i][j].value = cells[i][j].entryButton.text
                        cells[i][j].poss.clear()
                        cells[i][j].updateRelated(cells, blocks)
            if checkForFillableCells(cells):
                step += 1
                solveHistory.append(history(step, "Elimination", (i, j)))
            button.text = "Next Hint"
        else:
            findNextMove(cells, blocks)


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