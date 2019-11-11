"""Play a sound."""
from app import *

class Demo(App):
    def __init__(self):
        super().__init__()
        
        print('init =', pygame.mixer.get_init())
        print('channels =', pygame.mixer.get_num_channels())
        App.snd = pygame.mixer.Sound('5_app/rpgaudio.ogg')
        App.snd.play()
        print('length =', App.snd.get_length())

        Scene(caption='Sound mixer')
        Button('Stop', cmd='pygame.mixer.stop()')
        Button('Pause', cmd='pygame.mixer.pause()')
        Button('Unpause', cmd='pygame.mixer.unpause()')
        Button('Fadeout', cmd='pygame.mixer.fadeout(5000)')
        Button('Play', cmd='App.snd.play()')
        Button('Volume 0.1', cmd='App.snd.set_volume(0.1)', pos=(200, 20))
        Button('Volume 0.3', cmd='App.snd.set_volume(0.3)')
        Button('Volume 1.0', cmd='App.snd.set_volume(1.0)')

if __name__ == '__main__':
    Demo().run()