Drawing graphics primitives
============================

The ``pygame.draw`` module allows to draw simple shapes to a surface. 
This can be the screen surface or any Surface object such as an image or drawing:

- rectangle
- polygon
- circle
- ellipse

The functions have in common that they:

- take a **Surface** object as first argument
- take a color as second argument
- take a width parameter as last argument
- return a **Rect** object which bounds the changed area

the following format::

    rect(Surface, color, Rect, width) -> Rect
    polygon(Surface, color, pointlist, width) -> Rect
    circle(Surface, color, center, radius, width) -> Rect

Most of the functions take a width argument. If the width is 0, the shape is filled.

Draw solid and outlined rectangles
----------------------------------

The following draws first the background color and then adds three overlapping solid rectangles
and next to it three oulined overlapping rectangles with increasing line width::

    screen.fill(background)
    pygame.draw.rect(screen, RED, (50, 20, 120, 100))
    pygame.draw.rect(screen, GREEN, (100, 60, 120, 100))
    pygame.draw.rect(screen, BLUE, (150, 100, 120, 100))

    pygame.draw.rect(screen, RED, (350, 20, 120, 100), 1)
    pygame.draw.rect(screen, GREEN, (400, 60, 120, 100), 4)
    pygame.draw.rect(screen, BLUE, (450, 100, 120, 100), 8)

.. image:: draw1.png

Try to modifiy the parameters and play with the drawing function.


Draw solid and outlined ellipses
--------------------------------

The following code draws first the background color and then adds three overlapping solid ellipses
and next to it three oulined overlapping ellipses with increasing line width::

    screen.fill(background)
    pygame.draw.ellipse(screen, RED, (50, 20, 160, 100))
    pygame.draw.ellipse(screen, GREEN, (100, 60, 160, 100))
    pygame.draw.ellipse(screen, BLUE, (150, 100, 160, 100))
    
    pygame.draw.ellipse(screen, RED, (350, 20, 160, 100), 1)
    pygame.draw.ellipse(screen, GREEN, (400, 60, 160, 100), 4)
    pygame.draw.ellipse(screen, BLUE, (450, 100, 160, 100), 8)

    pygame.display.update()

.. image:: draw2.png

Detect the mouse
----------------

Pressing the mouse buttons produces MOUSEBUTTONDOWN and MOUSEBUTTONUP events.
The flollowing code in the event loop detects them and writes the event to the console::

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            print(event)
        elif event.type == MOUSEBUTTONUP:
            print(event)   

Pressing the mouse buttons produces this kind of events::

    <Event(5-MouseButtonDown {'pos': (123, 88), 'button': 1, 'window': None})>
    <Event(6-MouseButtonUp {'pos': (402, 128), 'button': 1, 'window': None})>
    <Event(5-MouseButtonDown {'pos': (402, 128), 'button': 3, 'window': None})>
    <Event(6-MouseButtonUp {'pos': (189, 62), 'button': 3, 'window': None})>

Just moving the mouse produces a MOUSEMOTION event.
The following code detects them an writes the event to the console::

        elif event.type == MOUSEMOTION:
            print(event)

Moving the mosue produces this kind of event::

    <Event(4-MouseMotion {'pos': (537, 195), 'rel': (-1, 0), 'buttons': (0, 0, 0), 'window': None})>
    <Event(4-MouseMotion {'pos': (527, 189), 'rel': (-10, -6), 'buttons': (0, 0, 0), 'window': None})>
    <Event(4-MouseMotion {'pos': (508, 180), 'rel': (-19, -9), 'buttons': (0, 0, 0), 'window': None})>


Draw a rectangle with the mouse
-------------------------------

We can use this three events to draw a rectangle on the screen.
We define the rectangle by its diagonal start and end point.
We also need a flag which indicates if the mouse button is down and if we are drawing::

    start = (0, 0)
    size = (0, 0)
    drawing = False

When the mouse button is pressed, we set start and end to the current mouse position
and indciate with the flag that the drawing mode has started::

    elif event.type == MOUSEBUTTONDOWN:
        start = event.pos
        size = 0, 0
        drawing = True

When the mouse button is released, we set the end point
and indicate with the flag that the drawing mode has ended::

    elif event.type == MOUSEBUTTONUP:
        end = event.pos
        size = end[0] - start[0], end[1] - start[1]
        drawing = False

When the mouse is moving we have first to check if we are in 
drawing mode. If yes, we set the end position to the current mouse position::

    elif event.type == MOUSEMOTION:
        if drawing:
            end = event.pos
            size = end[0] - start[0], end[1] - start[1]

Finally we draw the rectangle to the screen. First we fill in
the background color. Then we calculate the size of the rectangle.
Finally we draw it, and at the very last we update the screen::

    screen.fill(GRAY)
    pygame.draw.rect(screen, RED, (start, size), 2)
    pygame.display.update()

.. image:: mouse2.png


Draw multiple shapes
--------------------

To draw multiple shapes, we need to place them into a list. Besides variables for 
``start``, ``end`` and ``drawing`` we add a rectangle list::

    start = (0, 0)
    size = (0, 0)
    drawing = False
    rect_list = []

When drawing of an object (rectangle, circle, etc.) is done, as indicated by a
MOUSEBUTTONUP event, we create a rectangle and append it to the rectangle list::

    elif event.type == MOUSEBUTTONUP:
        end = event.pos
        size = end[0]-start[0], end[1]-start[1]
        rect = pygame.Rect(start, size)
        rect_list.append(rect)
        drawing = False

In the drawing code, we first fill the background color, then iterate through the 
rectagle list to draw the objects (red, thickness=3), and finally we draw the current rectangle which
is in the process of being drawn (blue, thickness=1)::

    screen.fill(GRAY)
    
    for rect in rect_list:
        pygame.draw.rect(screen, RED, rect, 3)
    pygame.draw.rect(screen, BLUE, (start, size), 1)
    
    pygame.display.update()

.. image:: mouse3.png


The App class
--------------

The basic structure of a game is always the same.
We create a ``App`` class from which we can sub-class our applications.

The constructor method

* initilizes the module
* creates a display window, stored as class variable ``App.screen``
* defines a background color
* defines an empty ``objects`` list::

    class App():
        """Define the main game object and its attributes."""
        def __init__(self):
            pygame.init()
            App.screen = pygame.display.set_mode((640, 240))
            self.bg_color = WHITE
            self.objects = []

The ``run()`` method enters the game loop. Only the QUIT event
is handled. All other events are sent to the ``on_event`` function::

    def run(self):
        """Run the main event loop.
        Handle the QUIT event and call ``on_event``. """
        running = True
        while running:
            for event in pygame.event.get():

                if event.type == QUIT:
                    running = False
                else:
                    self.on_event(event)
            self.draw()

If a game has events and interacts with the user then the ``on_event```
method must be implemented::

    def on_event(self, event):
        """Implement an event handler."""
        pass

The ``draw()`` method 

* draws the background
* draws all the objects in the ``objects`` list
* updates (flips) the display::

    def draw(self):
        """Draw the game objects to the screen."""
        self.screen.fill(self.bg_color)
        for object in self.objects:
            object.draw()
        pygame.display.flip()

.. automodule:: draw5

.. autoclass:: LineDemo
   :members:

.. image:: draw5.png


Text demo
---------

The basic structure of a game is always the same.
We create a ``App`` class from which we can sub-class.

 .. automodule:: draw6

 .. autoclass:: Text
    :members:

.. autoclass:: ListLabel

.. autoclass:: TextDemo
   :members:

.. image:: draw6.png

Drawing shapes
--------------

The **pygame.draw** module has methods for drawing shapes to the screen:

* pygame.draw.rect
* pygame.draw.polygon
* pygame.draw.circle

The methods only draw the shape once. Using an object-oriented approach we are going 
to define classes for each shape. There is a common class which we call ``Shape`` 

The class defintion begins with a couple of **class attributes**::

    class Shape:
        """Base class for geometric shapes having size, color and thickness."""
        size = [50, 20]  # default size
        color = BLUE     # default color
        d = 0            # default thickness
        v = [0, 0]       # default speed

The constructor methods finds the attribute values for the shape either from the 
class attribute, or from the argument passed::

        if pos != None:
            App.pos = list(pos)
        self.pos = App.pos[:]

        if size != None:
            Shape.size = list(size)
        self.size = Shape.size[:]
        App.pos[1] += Shape.size[1] 
        
        if color != None:
            Shape.color = color
        self.color = Shape.color

        if d != None:
            Shape.d = d
        self.d = Shape.d

        if v != None:
            Shape.v = list(v)
        self.v = Shape.v

At the end we define the enclosing rectangle which is used by some of the drawing methods.
Finally the object is appended to the objects list::

        self.rect = Rect(self.pos, self.size)
        App.objects.append(self)

The ``draw()`` method needs to be instantiated separately for each object type::

    def draw():
        pass

Rectangles ane Ellipses
-----------------------

This are two derived classes:

.. currentmodule:: pygamelib

.. autoclass:: Rectangle
    :members:

.. autoclass:: Ellipse
    :members:
 
.. autoclass:: Rectangle
    :members:
 
.. image:: draw7.png


Polygons, Arcs and Lines
------------------------

This are some more derived classes:

.. autoclass:: Polygon
    :members:

.. autoclass:: Arc
    :members:
 
.. autoclass:: Line
    :members:
 
.. image:: draw8.png


Randomly moving shapes
----------------------

In order to move the shapes, we add an ``update()`` method to ``Shape``::

    def update(self):
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        if not 0 < self.pos[0] < App.screen.get_width()-self.size[0]:
            self.v[0] *= -1
        if not 0 < self.pos[1] < App.screen.get_height()-self.size[1]:
            self.v[1] *= -1
        self.rect.topleft = self.pos

.. image:: draw9.png