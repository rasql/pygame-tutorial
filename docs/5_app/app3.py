from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        
        Scene(caption='Intro')
        Text('Scene 0')
        Text('Introduction screen the app')

        Scene(bg=Color('yellow'), caption='Options')
        Text('Scene 1')
        Text('Option screen of the app')

        Scene(bg=Color('green'), caption='Main')
        Text('Scene 2')
        Text('Main screen of the app')
        
        App.scene = App.scenes[0]

if __name__ == '__main__':
    Demo().run()