import kivy
kivy.require("1.10.1")

from kivy.config import Config

# Config.set('graphics', 'resizable', '0')
# Config.set('graphics', 'width', '1000')
# Config.set('graphics', 'height', '600')

from kivy.core.window import Window

import cProfile

from kivy.app import App
from kivy.lang import Builder
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.colorpicker import Color
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.uix.behaviors import DragBehavior
from kivymd.theming import ThemeManager

from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionItem
from kivy.uix.actionbar import ActionSeparator
from kivy.uix.actionbar import ActionOverflow

from PayloadActionButton import PayloadActionButton
from PayloadActionGroup import PayloadActionGroup
from PayloadActionPrevious import PayloadActionPrevious

from PayloadButton import PayloadButton

from MasterWindow import MasterWindow

from HoverEvent import HoverEvent

from kivy.properties import ObjectProperty, StringProperty

from LoginScreen import LoginScreen

from Menu import Menu

class vButton(Button, HoverEvent):
  pass
    
  def on_enter(self, *args):
    pass

  def on_leave(self, *args):
    pass

class PayloadLabel(Label):
    def on_touch_down(self, touch):
        print("\nPayloadLabel.on_touch_down:")

        if self.collide_point(*touch.pos):
            print("\ttouch.pos =", touch.pos)
            self.touch_x, self.touch_y = touch.spos[0], touch.spos[1]
            return True
        return super(PayloadLabel, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        print("\nPayloadLabel.on_touch_move:")

        if self.collide_point(*touch.pos):
            print("\ttouch.pos =", touch.pos)
            Window.top = self.touch_y + touch.spos[0]
            Window.left = self.touch_x + touch.spos[1]
            return True
        return super(PayloadLabel, self).on_touch_move(touch)

class PayloadBoxLayout(BoxLayout):
    pass

class PayloadStackLayout(StackLayout):
  def __init__(self):
    super(PayloadStackLayout, self).__init__()

class PayloadHorizontalLayout(StackLayout):
  def __init__(self):
    super(PayloadHorizontalLayout, self).__init__()

class Payload(App):
  icon = 'Vault.ico'
  title = "Payload"

  theme = ThemeManager()
#   Window.borderless = "0"
  def __init__(self):
    super(Payload, self).__init__()
    self.master = BoxLayout(orientation = "vertical")
    self.master.add_widget(Menu(), 0)

    self.main_frame = MasterWindow()
    self.main_frame.padding = [150, 0, 0, 0]
    self.master.add_widget(self.main_frame)

    self.main_panel = BoxLayout(orientation = "horizontal")
    self.main_frame.add_widget(self.main_panel)
    self.main_window = BoxLayout(orientation = "vertical")
    self.main_window.padding = [150, 0, 0, 0]
    self.main_frame.add_widget(self.main_window)

    self.panel = PayloadStackLayout()
    self.main_panel.add_widget(self.panel)

    self.footer = PayloadHorizontalLayout()
    self.main_window.add_widget(self.footer)

  def on_start(self):
    self.profile = cProfile.Profile()
    self.profile.enable()
    
  def on_pause(self):
    return True
  
  def on_resume(self):
    pass

  def on_stop(self):
    self.profile.disable()
    self.profile.dump_stats("Payload.profile")

    def on_touch_down(self, touch):
        print("\nPayloadLabel.on_touch_down:")

        if self.collide_point(*touch.pos):
            print("\ttouch.pos =", touch.pos)
            self.touch_x, self.touch_y = touch.spos[0], touch.spos[1]
            return True
        return super(Payload, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        print("\nPayloadLabel.on_touch_move:")

        if self.collide_point(*touch.pos):
            print("\ttouch.pos =", touch.pos)
            Window.top = self.touch_y + touch.spos[0]
            Window.left = self.touch_x + touch.spos[1]
            return True
        return super(Payload, self).on_touch_move(touch)

  def build(self):
    # App.display_settings()
    self.theme.theme_style = "Dark"

    btn = vButton(text = "A", size_hint = (None, None))
    btn1 = vButton(text = "B", size_hint = (None, None))
    btn2 = vButton(text = "C", size_hint = (None, None))
    btn3 = vButton(text = "D", size_hint = (None, None))
    btn4 = vButton(text = "E", size_hint = (None, None))

    btn5 = vButton(text = "F", size_hint = (None, None))
    btn6 = vButton(text = "G", size_hint = (None, None))
    btn7 = vButton(text = "H", size_hint = (None, None))
    btn8 = vButton(text = "I", size_hint = (None, None))
    btn9 = vButton(text = "J", size_hint = (None, None))
    btn10 = vButton(text = "K", size_hint = (None, None))
    btn11 = vButton(text = "L", size_hint = (None, None))

    self.panel.add_widget(btn)
    self.panel.add_widget(btn1)
    self.panel.add_widget(btn2)
    self.panel.add_widget(btn3)
    self.panel.add_widget(btn4)

    self.footer.add_widget(btn5)
    self.footer.add_widget(btn6)
    self.footer.add_widget(btn7)
    self.footer.add_widget(btn8)
    self.footer.add_widget(btn9)
    self.footer.add_widget(btn10)
    self.footer.add_widget(btn11)

    return self.master

Builder.load_string('''
<vButton>:
    background_color: 1, 1, 1, 0
    canvas.before:
        Color:
            rgba: (.35,.35,.35, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]

    color: 1, 1, 1, 1
    size: 75, 75

    # on_enter: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_enter: self.background_color = 1 / 255, 1 / 255, 1 / 255, 0.05
    # on_leave: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_leave: self.background_color = 1, 1, 1, 0
    # on_press: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_press: self.background_color = 1 / 255, 1 / 255, 1 / 255, 0.1
    # on_press: self.color = (1, 1, 1, 1)
    on_release: self.background_color = 1, 1, 1, 0
    on_release: self.background_normal = "atlas://data/images/defaulttheme/button"

<PayloadStackLayout>:
    orientation: "tb-lr"
    background_color: (1,1,1,1)
    spacing: 25, 25
    padding: 35, 35, 0, 0
    # pos_hint: {'left' : 1}
    canvas.before:
        Color:
            rgba: 150 / 255, 150 / 255, 150 / 255, 1 
        Rectangle:
            pos: self.pos
            size: 150, self.height

<PayloadHorizontalLayout>:
    orientation: "lr-bt"
    background_color: (1,1,1,1)
    spacing: 25, 25
    padding: 75, 10, 10, 10
    # pos_hint: {'left' : 1}
    canvas.before:
        Color:
            rgba: 125 / 255, 125 / 255, 125 / 255, 1 
        Rectangle:
            pos: self.pos
            size: self.width, 100

<PayloadButton>:
    # color: 255, 255, 255, 1
    
    background_color: 1, 1, 1, 1

    on_enter: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_enter: self.background_color = 1, 1, 1, 0.75
    on_leave: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_leave: self.background_color = 1, 1, 1, 1
    on_press: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_press: self.background_color = 1 / 255, 1 / 255, 1 / 255, 0.1
    on_press: self.color = (1, 1, 1, 0.25)
    on_release: self.background_color = 1, 1, 1, 1
    on_release: self.background_normal = "atlas://data/images/defaulttheme/button"

    # size: 150, 0.0
    size_hint: 1.0, 1.0

<MasterWindow>:
    size_hint: 1.0, 1.0
    canvas.before:
        Color:
            rgba: 50 / 255, 50 / 255, 50 / 255, 1
        Rectangle:
            pos: self.pos
            size: self.size

<PayloadActionButton>:
    on_enter: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_enter: self.background_color = 1, 1, 1, 0.25
    on_leave: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_press: self.background_normal = "atlas://data/images/defaulttheme/button"
    on_press: self.background_color = 1, 1, 1, 0
    on_press: self.color = (1, 1, 1, 1)
    on_release: self.background_color = 1, 1, 1, 0
    on_release: self.background_normal = "atlas://data/images/defaulttheme/button"

<Menu>:
    pos_hint: {'top' : 1}
    height: 50
    padding: [10, 0, 10, 0]
    # padding: 0, 0, 0, 0
    # spacing: 100
    ActionView:
        ActionPrevious:
            title: " " * 3 + "Snow"
            with_previous: True
            app_icon: 'Snow.png'
            app_icon_width: 400
            app_icon_height: 500
            on_press: self.background_color = 1, 1, 1, 0
            on_press: self.background_color = 1, 1, 1, 0
        ActionOverflow:
        PayloadActionGroup:
            text: 'File' 
            mode: 'spinner'
            PayloadActionButton:
                important: True
                text: 'Important'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Option 2'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Option 3'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Option 4'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1

        PayloadActionGroup:
            text: 'Edit' 
            mode: 'spinner'
            PayloadActionButton:
                text: 'Option 1'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Option 2'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Option 3'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Option 4'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1

        PayloadActionGroup:
            text: 'Tools' 
            mode: 'spinner'
            PayloadActionButton:
                text: 'Tool 1'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Tool 2'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Tool 3'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Tool 4'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1

        PayloadActionGroup:
            text: 'Help' 
            mode: 'spinner'
            PayloadActionButton:
                text: 'About'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
            PayloadActionButton:
                text: 'Close'
                background_color: 1, 1, 1, 1
                size_hint: None, None
                size: 100, 50
                on_leave: self.background_color = 1, 1, 1, 1
                on_press: App.get_running_app().stop()


''')