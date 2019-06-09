import kivy

kivy.require("1.10.1")


from kivy.uix.button import Button
from HoverEvent import HoverEvent
from kivy.uix.floatlayout import FloatLayout

class PrimaryPanel(FloatLayout):
  def __init__(self, **input): 
    super(PrimaryPanel, self).__init__()