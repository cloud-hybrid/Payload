
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.button import Button


class HoverGUIBehavior(object):
    #__author__ = 'Olivier POYEN'
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
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverGUIBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
#==========================================================
        # Insert this statement to unbind itself its
        # parent does not exist
        if not self.parent:
            print("No self.parent")
            Window.unbind(mouse_pos=self.on_mouse_pos)
            return
#==========================================================
        pos = args[1]
        inside = self.collide_point(*pos)
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

class HoverButton(Button, HoverGUIBehavior):

    def on_enter(self, *args, **kwargs):
        print("I'm still here!")
        if not self.parent: # Find someway to remove itself
            print()
            print('self = ' + str(self))
            print("I'm definitely still here!")
            return
        self.ref_x = self.x
        self.ref_y = self.y

        self.anim = Animation(x = self.x -10 ,y = self.y - 10, duration=1.0, t='out_bounce') + Animation(x = self.x + 10, y = self.y + 10, duration=1.0, t='out_bounce')
        self.anim.repeat = True
        self.anim.start(self)

    def on_leave(self, *args):
        if not self.parent: # Find someway to remove itself 
            print()
            print('self = ' + str(self))
            print("I'm definitely still here!")
            return
        if self.anim:
            self.anim.cancel(self)
            return_anim = Animation(pos = (self.ref_x, self.ref_y), duration = 0.35, t='out_bounce')
            return_anim.start(self)

