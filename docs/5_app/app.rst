Making apps with Pygame
=======================

In this section we are going to create applications and games with Pygame. From here on we will be 
using an object-oriented programming (OOP) approach.

Pygame only allows to create one single window. Different from other applications,
those based on Pygame cannot have multiple windows. If for example dialog window is needed, it must be displayed within the main window.

Within an application we provide multples scenes (environments, rooms, or levels).
Each scene contains different objects such as:

- text
- sprites (images)
- GUI elements (buttons, menus)
- shapes (rectangles, circles)

Create the App class
-------------

The basis for a game or application is the ``App`` class. The first thing to do is to import 
the ``pygame`` module, as well as a series of useful constants::

    import pygame
    from pygame.locals import *

Then we create define the App class which initializes Pygame and opens a the app 
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


Add the Text class
------------------

Now we add some text to the screen. We create a Text class from which we can 
instantiate text objects::

    class Text:
        """Create a text object."""

        def __init__(self, text, pos, **options):
            self.text = text
            self.pos = pos

            self.fontname = None
            self.fontsize = 72
            self.fontcolor = Color('black')
            self.set_font()
            self.render()

The ``Font`` object needs to be created initially and everytime
the font name or the font size changes::

    def set_font(self):
        """Set the Font object from name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

The text needs to be rendered into a surface object, an image. This needs to be
done only once, or whenever the text changes::

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

Drawing the text means blitting it to the application screen::

    def draw(self):
        """Draw the text image to the screen."""
        App.screen.blit(self.img, self.rect)

This is the result:

.. image:: app2.png

Add the Scene class
-------------------

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

Then we set a scene id, which is kept as class attribute of the Scene class.
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

.. image:: app5.*


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





