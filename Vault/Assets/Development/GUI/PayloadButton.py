import kivy

kivy.require("1.10.1")

from kivy.lang import Builder
from kivy.uix.colorpicker import Color
from kivy.uix.button import Button
from HoverEvent import HoverEvent

class PayloadButton(Button, HoverEvent):
  def __init__(self, **input): 
    super(PayloadButton, self).__init__()

  def on_enter(self, *args):
    pass

  def on_leave(self, *args):
    pass