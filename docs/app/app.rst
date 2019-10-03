Making apps with Pygame
=======================

In this tutorial we are going to create applications and games with Pygame.
Pygame only allows to create one single window. A game or application cannot
have multiple windows. If a dialog window is needed, it must be displayed within the main window.

Within a game we will need multples scenes (sometimes called rooms, or levels).
Each scene contains objects with can be :

- text
- sprites (images)
- GUI elements (buttons, menus)
- shapes (rectangles, circles)

The App class
-------------

The basis for a game or application is the ``App`` class. The first thing to do is to import 
the ``Pygame`` module, as well as a series of useful constants::

    import pygame
    from pygame.locals import *

Then we create define the App class which initializes pygame and opens a the app 
window::

    class App:
        """Create a single-window app with multiple scenes."""

        def __init__(self):
            """Initialize pygame and the application."""
            pygame.init()
            flags = RESIZABLE
            App.screen = pygame.display.set_mode((640, 240), flags)

            App.running = True 

Further we have to define the main event loop::

    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False
        pygame.quit()

At the end of the module we run a demo, if the programm is run directly and not 
imported as a module::

    if __name__ == '__main__':
        App().run()


Add text
--------

Now we add some text to the screen. We create a Text class from which we can 
instantiate text objects::

    class Text:
        """Create a text object which knows how to draw itself."""

        def __init__(self, text, pos, **options):
            """Instantiate and render the text object."""
            self.str = text
            self.pos = pos
            self.fontsize = 72
            self.fontcolor = Color('black')
            self.render()

The text needs to be rendered into a surface object, an image. This needs to be
done only once, or whenever the text changes::

    def render(self):
        """Render the string and create a surface object."""
        self.font = pygame.font.Font(None, self.fontsize)
        self.text = self.font.render(self.str, True, self.fontcolor)
        self.rect = self.text.get_rect()

Drawing the text means blitting it to the application screen::

    def draw(self):
        """Draw the text surface on the screen."""
        App.screen.blit(self.text, self.pos)


Create scenes
-------------

Most applications or games have different scenes, such as an introduction screen, 
an intro, and different game levels. So we are going to define the Scene class::

    class Scene:
        """Create a new scene (room, level, view)."""
        id = 0
        bg = Color('gray')

When creating a new scene, we append the scene to the applications scene list
and make this scene the current scene::

    def __init__(self, *args, **kwargs):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self

The we set a scene id, which is kept as class attribute of the Scene class.
Then we set the nodes list to the empty list and set the background color::

        # Set the instance id and increment the class id
        self.id = Scene.id
        Scene.id += 1
        self.nodes = []
        self.bg = Scene.bg

The scene object knows how to draw itself. It first fills the background with the 
background color, then draws each nodes and finally flips the display to update the
screen::

    def draw(self):
        """Draw all objects in the scene."""
        App.screen.fill(self.bg)
        for node in self.nodes:
            node.draw()
        pygame.display.flip()

The string representation of the scene is *Scene* followed by its ID number::

    def __str__(self):
        return 'Scene {}'.format(self.id)

.. image:: app1.*


Shortcut keys
-------------

Key presses can be used to switch scenes, or to interact with the game,
or to run commands. We add the following code inside the event loop to
intercept the S key::

    if event.type == KEYDOWN:
        if event.key == K_s:
            print('Key press S')

The easiest way to represent shortcuts is under the form of a dictionary,
where the keys are associated with command strings. We add the following 
code inside the App init method::

    self.shortcuts = {K_ESCAPE: 'App.running=False',
                        K_p: 'self.capture()',
                        K_w: 'self.where()',
                        K_s: 'self.next_scene()',
                        }

Inside the event loop we detect keydown events and call the key handler::

    if event.type == KEYDOWN:
        self.do_shortcuts(event)

The following method handles the shortcuts for simple keys or combinations of 
keys and modifier keys:: 

    def do_shortcuts(self, event):
        """Check if the key/mod combination is part of the shortcuts
        dictionary and execute it. More shortcuts can be added 
        to the ``self.shortcuts`` dictionary by the program."""
        k = event.key
        m = event.mod

        if k in self.shortcuts and m == 0 :
            exec(self.shortcuts[k])
        elif (k, m) in self.shortcuts:
            exec(self.shortcuts[k, m])





