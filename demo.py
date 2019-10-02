from pglib import *
from pglib.app import *
print(dir())

app = App()
s0 = Scene(caption='My Game', size=(300, 300))
Node()
Scene(bg=Color('pink'), caption='My Scene', size=(800, 600))
Node()
Node()
Node()

Scene(bg=Color('beige'), caption='Introduction', size=(640, 480))
Node()
Node()

App.scenes.append(s0)
App.scene = s0
app.run()