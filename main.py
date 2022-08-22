from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.lang import Builder

sudoku_toggles = []
selection_buttons = []
cell_data = [[None for i in range(9)] for j in range(9)]

class MainScreen(BoxLayout):
    def switch_active(self, togglebutton):
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
    

class SudokuButtons(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuButtons, self).__init__(**kwargs)

        for i in range(0, 9):
            for j in range(0, 9):
                size = dp(35)
                b = ToggleButton(size_hint=(None, None), size=(size, size))
                sudoku_toggles.append(b)
                self.add_widget(b)
                newCell = cell(i, j, b)
                cell_data[i][j] = newCell

class EntryLayout(BoxLayout):
    def run_solver(self, button):
        for i in range(9):
            for j in range(9):
                if cell_data[i][j].entryButton.text != "":
                    cell_data[i][j].value = cell_data[i][j].entryButton.text
                    cell_data[i][j].poss.clear()
                    cell_data[i][j].updateRelated()



class NumberEntry(GridLayout):
    def __init__(self, **kwargs):
        super(NumberEntry, self).__init__(**kwargs)

        for i in range(0, 10):
            size = dp(35)
            title = ""
            if i > 0:
                title = str(i)
            b = Button(text=title, size_hint=(None, None), size=(size, size), disabled = True, on_press = self.num_entry)
            selection_buttons.append(b)
            self.add_widget(b)

    def num_entry(self, button):
        for cell in sudoku_toggles:
            if cell.state == "down":
                cell.text = button.text
                cell.state = "normal"
                for butt in selection_buttons:
                    butt.disabled = True
                return
        for butt in selection_buttons:
            butt.disabled = True

class cell():
    def __init__(self, myRow, myColumn, myButton):
        self.row = myRow
        self.column = myColumn
        self.block = None
        self.poss = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.value = None
        self.entryButton = myButton
        if 0 < self.row < 3 and 0 < self.column < 3:
            self.block = "tl"
        elif 0 < self.row < 3 and 2 < self.column < 6:
            self.block = "tm"
        elif 0 < self.row < 3 and 5 < self.column < 9:
            self.block = "tr"
        elif 2 < self.row < 6 and 0 < self.column < 3:
            self.block = "ml"
        elif 2 < self.row < 6 and 2 < self.column < 6:
            self.block = "mm"
        elif 2 < self.row < 6 and 5 < self.column < 9:
            self.block = "mr"
        elif 5 < self.row < 9 and 0 < self.column < 3:
            self.block = "bl"
        elif 5 < self.row < 9 and 2 < self.column < 6:
            self.block = "bm"
        elif 5 < self.row < 9 and 5 < self.column < 9:
            self.block = "br"

    def updateRelated(self):
        for i in range(9):
            for j in range(9):
                if cell_data[i][j].row == self.row and cell_data[i][j].column == self.column:
                    pass
                elif cell_data[i][j].row == self.row or cell_data[i][j].column == self.column or cell_data[i][j].block == self.block:
                    cell_data[i][j].poss.remove(self.value)

    

class SudokuPartnerApp(App):
    def build(self):
        return MainScreen()




SudokuPartnerApp().run()