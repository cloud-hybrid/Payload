from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.properties import BooleanProperty

class HoverEvent(object):
  hovered = BooleanProperty(False)
  border_point = ObjectProperty(None)

  def __init__(self):
    self.register_event_type('on_enter')
    self.register_event_type('on_leave')
    Window.bind(mouse_pos = self.on_mouse_pos)
    super(HoverEvent, self).__init__()

  def on_mouse_pos(self, *args):
    if not self.get_root_window():
      return 
    position = args[1]

    inside = self.collide_point(*self.to_widget(*position))
    if self.hovered == inside:
      return

    self.border_point = position
    self.hovered = inside

    if inside:
      self.dispatch('on_enter')
    else:
      self.dispatch('on_leave')

  def on_enter(self):
    pass

  def on_leave(self):
    pass

from kivy.factory import Factory
Factory.register('HoverEvent', HoverEvent)