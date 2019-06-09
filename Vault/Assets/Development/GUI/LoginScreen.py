from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class LoginScreen(GridLayout):
  def __init__(self):
    super(LoginScreen, self).__init__()
    self.cols = 2

    self.add_widget(Label(text = "Email Address"))
    self.email = TextInput(multiline = False, size = (100, 100))
    self.add_widget(self.email)

    self.add_widget(Label(text = "Password"))
    self.password = TextInput(password = True, multiline = False)
    self.add_widget(self.password)

