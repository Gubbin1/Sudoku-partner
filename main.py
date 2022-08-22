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

        print(tb, tb.state, tb.text)
    
    

class SudokuButtons(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuButtons, self).__init__(**kwargs)

        for i in range(0, 81):
            size = dp(35)
            b = ToggleButton(size_hint=(None, None), size=(size, size))
            sudoku_toggles.append(b)
            self.add_widget(b)




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
    
    

class SudokuPartnerApp(App):
    def build(self):
        return MainScreen()




SudokuPartnerApp().run()