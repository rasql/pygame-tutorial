"""Define shortcut keys with modifiers."""

import pygame
from pygame.locals import *
from pygamelib import * 

d = {
    K_a:'print("A")',
    (K_a, KMOD_LSHIFT):'print("shift+A")',
    (K_a, KMOD_LCTRL):'print("ctrl+A")',
    (K_a, KMOD_LALT):'print("alt+A")',
    (K_a, KMOD_LMETA):'print("cmd+A")', 
    K_UP:'print("UP")',
    K_LEFT:'print("LEFT")',
}

class ShortcutDemo(App):
    def __init__(self):
        super(ShortcutDemo, self).__init__()
        Text('Shortcuts')
        Text('Press A, with shift, ctrl, alt and cmd', size=24)

    def on_event(self, event):
        if event.type == KEYDOWN:
            k = event.key
            m = event.mod
            if k in d and m == 0 :
                exec(d[k])
            elif (k, m) in d:
                exec(d[k, m])

if __name__ == '__main__':
    ShortcutDemo().run()