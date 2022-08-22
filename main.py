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

class MainScreen(BoxLayout):
    def switch_active(self, togglebutton):
        tb = togglebutton
        print(tb, tb.state, tb.text)

class SudokuButtons(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuButtons, self).__init__(**kwargs)

        for i in range(0, 81):
            size = dp(35)
            b = ToggleButton(text=str(i), size_hint=(None, None), size=(size, size))
            sudoku_toggles.append(b)
            self.add_widget(b)

class NumberEntry(GridLayout):
    def __init__(self, **kwargs):
        super(NumberEntry, self).__init__(**kwargs)

        for i in range(0, 10):
            size = dp(35)
            b = Button(text=str(i), size_hint=(None, None), size=(size, size), disabled = True)
            sudoku_toggles.append(b)
            self.add_widget(b)
    
    

class SudokuPartnerApp(App):
    def build(self):
        return MainScreen()




SudokuPartnerApp().run()