from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        
        Scene(caption='Intro')
        Text('Scene 0')
        Text('Introduction screen the app')
        Rectangle(Color('red'), Color('green'), 5)

        Scene(bg=Color('yellow'), caption='Options')
        Text('Scene 1')
        Text('Option screen of the app')

        Scene(bg=Color('lightgreen'), caption='Main')
        Text('Scene 2', cmd='print(self.text)')
        Text('Main screen of the app')
        Button('Scene', cmd='print(App.scene)')
        Button('Button 1', cmd='print(123)')
        Button('Button 2', cmd='print(self)')

        Button('Fullscreen', cmd='App.toggle_full_screen()', pos=(200, 20))
        Button('Hello', cmd='print("hello")')
        
        App.scene = App.scenes[0]

if __name__ == '__main__':
    Demo().run()