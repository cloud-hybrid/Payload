import kivy

kivy.require("1.10.1")

from kivy.lang import Builder
from kivy.uix.colorpicker import Color
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionItem
from HoverEvent import HoverEvent

class PayloadActionButton(Button, ActionItem, HoverEvent):
  def __init__(self, **input): 
    super(PayloadActionButton, self).__init__()

  def on_enter(self, *args):
    pass

  def on_leave(self, *args):
    pass

# Builder.load_string('''
# <PayloadActionButton>:
#     background_color: 1, 1, 1, 0

#     on_enter: self.background_normal = "atlas://data/images/defaulttheme/button"
#     on_enter: self.background_color = 1, 1, 1, 0.25
#     on_leave: self.background_normal = "atlas://data/images/defaulttheme/button"
#     on_press: self.background_normal = "atlas://data/images/defaulttheme/button"
#     on_press: self.background_color = 1, 1, 1, 0
#     on_press: self.color = (1, 1, 1, 1)
#     on_release: self.background_color = 1, 1, 1, 0
#     on_release: self.background_normal = "atlas://data/images/defaulttheme/button"
# ''')
