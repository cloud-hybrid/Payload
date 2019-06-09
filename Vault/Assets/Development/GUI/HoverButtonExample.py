import kivy
kivy.require("1.10.1")

import cProfile
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.colorpicker import Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.actionbar import ActionItem

from kivy.properties import ObjectProperty, StringProperty

from kivy.atlas import Atlas

class HoverBehavior(object):
  """Hover behavior.
  :Events:
      `on_enter`
          Fired when mouse enter the bbox of the widget.
      `on_leave`
          Fired when the mouse exit the widget 
  """

  hovered = BooleanProperty(False)
  border_point= ObjectProperty(None)
  '''Contains the last relevant point received by the Hoverable. This can
  be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
  '''

  def __init__(self, **kwargs):
    self.register_event_type('on_enter')
    self.register_event_type('on_leave')
    Window.bind(mouse_pos = self.on_mouse_pos)
    super(HoverBehavior, self).__init__(**kwargs)

  def on_mouse_pos(self, *args):
    if not self.get_root_window():
      return # do proceed if I'm not displayed <=> If have no parent
    pos = args[1]
    #Next line to_widget allow to compensate for relative layout
    inside = self.collide_point(*self.to_widget(*pos))
    if self.hovered == inside:
      #We have already done what was needed
      return
    self.border_point = pos
    self.hovered = inside
    if inside:
      self.dispatch('on_enter')
    else:
      self.dispatch('on_leave')

  def on_enter(self):
    pass

  def on_leave(self):
    pass

class PayloadActionButton(App, Button, ActionItem, HoverBehavior):
  def __init__(self):
    super(PayloadActionButton, self).__init__()

  def on_enter(self, *args):
      print("You are in, through this point", self.border_point)
      # Button().Color(0, 1, 1, 1.0)
      PayloadActionButton().background_color = [10, 10, 10, 1.0]

  def on_leave(self, *args):
      print("You left through this point", self.border_point)

  def getButtonname(self):
      return self.button_name

  def build(self):
      master = BoxLayout()



      return master

from kivy.factory import Factory
Factory.register('HoverBehavior', HoverBehavior)

if __name__=='__main__':
  from kivy.base import runTouchApp

  Builder.load_string('''
<PayloadActionButton>:
    text: "Button"
    pos_hint: {"center_x": 0.5, "center_y": 0.5}
    auto_scale: "both"
    display_border: False
    background_image: "payload-button-pressed.png"
    size_hint: None, None
    size: 150, 150

    on_enter: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_enter: self.background_color = 1, 1, 1, 0.9
    on_leave: self.background_color = 1, 1, 1, 1.0
    on_leave: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_press: self.background_color = 1, 1, 1, 0
    on_press: self.color = (255, 255, 255, 1)
    on_release: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_release: self.color = (1, 1, 1, 1)

    on_release: self.background_color = 1, 1, 1, 1
    canvas.before:
        Color:
            rgb: (1.0, 1.0, 1.0, 1.0)
        Rectangle:
            size: self.width, self.height
            pos: self.pos
    ''')

  from kivy.uix.floatlayout import FloatLayout
  fl = FloatLayout()
  fl.add_widget(PayloadActionButton())

runTouchApp(fl)
