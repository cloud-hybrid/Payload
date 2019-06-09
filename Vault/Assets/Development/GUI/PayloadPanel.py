import kivy

kivy.require("1.10.1")


from kivy.uix.button import Button
from HoverEvent import HoverEvent
from kivy.uix.floatlayout import FloatLayout

class PayloadPanel(FloatLayout):
  def __init__(self, **input): 
    super(PayloadPanel, self).__init__()