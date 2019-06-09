import kivy

kivy.require("1.10.1")

from kivy.lang import Builder
from kivy.uix.colorpicker import Color
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionPrevious
from HoverEvent import HoverEvent

class PayloadActionPrevious(ActionPrevious, HoverEvent):
  def __init__(self, **input): 
    super(PayloadActionPrevious, self).__init__()

  def on_enter(self, *args):
      print("You are in, through this point", self.border_point)
      # Button().Color(0, 1, 1, 1.0)
      # PayloadActionButton().background_color = [10, 10, 10, 1.0]

  def on_leave(self, *args):
      print("You left through this point", self.border_point)

# Builder.load_string('''
# <PayloadActionPrevious>:
#     # title: " " * 3 + "Snow"
#     with_previous: True
#     # app_icon: 'Snow.png'
#     # app_icon_width: 400
#     # app_icon_height: 500
#     # text: "Button"
#     # pos_hint: {"center_x": 0.5, "center_y": 0.5}
#     # auto_scale: "both"
#     # display_border: False
#     # size_hint: None, None
#     # size: 50, 50

#     # on_enter: self.background_color = 1, 1, 1, 0.35
#     # on_leave: self.background_color = 1, 1, 1, 1.0
#     # on_press: self.background_color = 1, 1, 1, 0
#     # on_release: self.color = (1, 1, 1, 1)
#     # on_release: self.background_color = 1, 1, 1, 1
# ''')

# # from kivy.factory import Factory
# # Factory.register('PayloadActionPrevious', PayloadActionPrevious)