"""Display text editable with a cursor."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        Scene(caption='Text with cursor')
        Text('This is a text object', size=(600, 0))
        TextEdit('Text with cmd (press Enter)', cmd='print(self.text)', fontsize=12, size=(400, 30))
        TextEdit('You can edit this', fontcolor=Color('white'))
        TextEdit('It remembers the cursor position', fontsize=48)

if __name__ == '__main__':
    Demo().run()