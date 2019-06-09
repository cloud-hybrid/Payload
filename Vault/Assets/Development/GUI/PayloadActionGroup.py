import kivy

kivy.require("1.10.1")

from kivy.lang import Builder
from kivy.uix.colorpicker import Color
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionGroup
from HoverEvent import HoverEvent

class PayloadActionGroup(ActionGroup, HoverEvent):
  def __init__(self, **input): 
    super(PayloadActionGroup, self).__init__()

  def on_enter(self, *args):
    pass

  def on_leave(self, *args):
    pass

Builder.load_string('''
<PayloadActionGroup>:
    text: "Button"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    auto_scale: "both"
    display_border: False
    size_hint: None, None
    size: 50, 50

    on_enter: self.background_color = 1, 1, 1, 0.35
    on_leave: self.background_color = 1, 1, 1, 1.0
    on_press: self.background_color = 1, 1, 1, 0
    on_release: self.color = (1, 1, 1, 1)
    on_release: self.background_color = 1, 1, 1, 1
''')

from kivy.factory import Factory
Factory.register('PayloadActionGroup', PayloadActionGroup)