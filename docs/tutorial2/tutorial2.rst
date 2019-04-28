Drawing primitives
==================

The ``draw`` module allows to draw simple shapes to a surface:

* rectangle
* polygon
* circle
* ellipse
* arc
* line
* lines

The functions have the following format::

    rect(Surface, color, Rect, width) -> Rect
    polygon(Surface, color, pointlist, width) -> Rect
    circle(Surface, color, center, radius, width) -> Rect

Most of the functions take a width argument. If the width is 0, the shape is filled.

.. automodule:: draw1

.. autoclass:: Game
   :members:

.. image:: draw1.png

Draw a rectangle
----------------

In the next example we use the arrow keys to move the rectangle and alt+arrow to resize the rectangle.
We define a dictionary which associates the 4 arrow keys with a displacement vector::

    d = {K_UP:(0, -10), K_DOWN:(0, 10), K_LEFT:(-10, 0), K_RIGHT:(10, 0)}

The code for the movement becomes now very simple::

    if event.type == pygame.KEYDOWN:
        if event.key in d:
            vec = d[event.key]
            if event.mod & KMOD_ALT:
                self.rect.inflate_ip(vec)
            else:
                self.rect.move_ip(vec)

We define also a color dictionary which associations a character key with a color::

    color = {K_r:RED, K_b:BLUE, K_g:GREEN, K_m:MAGENTA, 
                K_c:CYAN, K_y:YELLOW, K_k:BLACK, K_w:WHITE}

Again, when using dictionaries, the code becomes very short and simple::

    if event.key in color:
        if event.mod & KMOD_ALT:
            self.bg = color[event.key]
        else:
            self.col = color[event.key]

.. automodule:: draw2

.. autoclass:: Game
   :members:

.. image:: draw2.png

Place a rectangle with the mouse
--------------------------------

In the next program we use the mouse button to draw a rectangle.

 .. automodule:: draw3

.. autoclass:: Game
   :members:

.. image:: draw3.png

Draw lines
----------

 .. automodule:: draw4

.. autoclass:: Game
   :members:

.. image:: draw4.png
