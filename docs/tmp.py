import pygame

options = {'kep':False}
if 'keep' in options:
    print(options['keep'])
else:
    print('not')

class RadioButton:

    def __init__(self, items, i=-1):
        self.items = items
        self.i = i

class CheckButton:

    def __init__(self, items, sel):
        self.items = items
        self.sel = sel
        self.order = range(len(sel))

        