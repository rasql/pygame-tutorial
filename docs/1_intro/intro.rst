Introduction to Pygame
======================

Pygame is a multimedia library for Python for making:

- games
- multimedia applications

It is a wrapper around the SDL (Simple DirectMedia Layer) library.
In this section we indroduce the basics of pygame functions without defining classes and objects.


Import the module
-----------------

In order to use the methods defined in the pygame package, the pygame module must first be imported::

    import pygame

The import statement writes the pygame version and the following text to the console::

    pygame 1.9.5
    Hello from the pygame community. https://www.pygame.org/contribute.html

The pygame import statement is always placed at the beginning of the program.
The effect is to import pygame classes, methods and attributes into the current name space. 
Now this new methods can be called via ``pygame.method_name()``. 

For exemple we can now initialize the pygame submodules with the following command::

    pygame.init()

Then we set the screen size with the function ``display.set_mode()``. This function returns 
a ``Surface`` object wich we assign to the variable ``screen``. This variable will be one of the most 
important and most used variables. It is the one variable which represents what we see in the application::

    screen = pygame.display.set_mode((640, 240))

You can now run this program and test it. At this moment it does very little.
It opens a window and closes it immediately. 

Show the event loop
-------------------

One of the essential parts of any interactive application is the event loop. 
Reacting to events allows the user to interact with the application.
Events are the things that can happen in a program, such as a 

- mouse click, 
- mouse movement, 
- keyboard press,
- joystick action.

The following is an infinite loop which prints all events to the console::

    while True:
        for event in pygame.event.get():
            print(event)

Try to move the mouse, click a mouse button, or type something on the keyboard.
Every action you do produces an event which will be sent and printed on the console.
This will look something like this::

    <Event(4-MouseMotion {'pos': (173, 192), 'rel': (173, 192), 'buttons': (0, 0, 0), 'window': None})>
    <Event(2-KeyDown {'unicode': 'a', 'key': 97, 'mod': 0, 'scancode': 0, 'window': None})>
    <Event(3-KeyUp {'key': 97, 'mod': 0, 'scancode': 0, 'window': None})>
    <Event(12-Quit {})>

As we are in an infite loop, it is impossible to quit this program from within the application.
In order to quit the program, make the console the active window and type ``ctrl-C``. 
This will write the following message to the console::

    ^CTraceback (most recent call last):
    File "/Users/raphael/GitHub/pygame-tutorial/docs/tutorial1/intro1.py", line 7, in <module>
        for event in pygame.event.get():
    KeyboardInterrupt

Quit the event loop properly
----------------------------

In order to quit the application properly, from within the application, 
by using the window close button (QUIT event), we modify the event loop. 
First we introduce the boolean variable ``running`` and set it 
to ``True``. Within the event loop we check for the QUIT event. 
If it occurs, we set ``running`` to ``False``::

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

Once the event loop, we call the ``pygame.quit()`` function to end the application 
correctly.

.. image:: intro2.png

Define colors
-------------

Colors are defined as tuples of the base colors red, green and blue. 
This is called the **RGB model**. 
Each base color is represented as a number between 0 (minimum) and 255 (maximum)
which occupies 1 byte in memory. An RGB color is thus represented as a 3-byte value.
Mixing two or more colors results in new colors. 
A total of 16 million different colors can be represented this way.

.. image:: AdditiveColorMixing.png
   :scale: 50 %

Let's define the base colors as tuples. Since these are constants, 
we are going to use capitals. At the beginning of the program we add::

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

Further we define the colors obtained by mixing two or more of the base colors::

    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)

Inside the event loop, at its end we add the following::

    screen.fill(YELLOW)
    pygame.display.update()

The method ``fill(color)`` fills the whole screen with the specified color. 
At this point nothing will be displayed. In order to show anything, the function
``pygame.display.update()`` must be called.

.. image:: intro3.png

Switch the background color
---------------------------

At the beginning of the program we add a new veriable ``background`` 
and initialze it to gray::

    background = GRAY

Within the event loop we are looking now for ``KEYDONW`` events. 
If found, we check if the R or G keys have been pressed and change the 
background color to red (R) and green (G). This is the code added in the event loop::

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                background = RED
            elif event.key == pygame.K_g:
                background = GREEN

In the drawing section we use now the variable ``background`` representing the 
background color::

    screen.fill(background)
    pygame.display.update()

Test the program. 
Pressing the R and G keys allows you to switch the background color.

Import pygame.locals
--------------------

The ``pygame.locals`` module contains some 280 constants used and defined by pygme. 
Placing this statement at the beginning of your programm imports them all::

    import pygame
    from pygame.locals import *

We find the key modifiers (alt, ctrl, cmd, etc.) ::

    KMOD_ALT, KMOD_CAPS, KMOD_CTRL, KMOD_LALT, 
    KMOD_LCTRL, KMOD_LMETA, KMOD_LSHIFT, KMOD_META, 
    KMOD_MODE, KMOD_NONE, KMOD_NUM, KMOD_RALT, KMOD_RCTRL, 
    KMOD_RMETA, KMOD_RSHIFT, KMOD_SHIFT, 
    
the number keys::

    K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, 

the special character keys::

    K_AMPERSAND, K_ASTERISK, K_AT, K_BACKQUOTE, 
    K_BACKSLASH, K_BACKSPACE, K_BREAK, 

the function keys::

    K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, 
    K_F9, K_F10, K_F11, K_F12, K_F13, K_F14, K_F15

the letter keys of the alphabet::

    K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, 
    K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, 
    
Instead of writing ``pygame.KEYDOWN`` we can now just write ```KEYDOWN``.


Use a dictionary to decode keys
-------------------------------

The easiest way to decode many keys, is to use a dictionary. 
Instead of defining many if-else cases, we just create a dictionary with the keyboard key entries.
In this exemple we want to associate 8 different keys with 8 different background colors. 
At the beginning of the programm we define this key-color dictionary::

    key_dict = {K_k:BLACK, K_r:RED, K_g:GREEN, K_b:BLUE, 
        K_y:YELLOW, K_c:CYAN, K_m:MAGENTA, K_w:WHITE}

    print(key_dict)

Printing the dictionary to the console gives this result::
    
    {107: (0, 0, 0), 114: (255, 0, 0), 103: (0, 255, 0), 98: (0, 0, 255), 
    121: (255, 255, 0), 99: (0, 255, 255), 109: (255, 0, 255), 119: (255, 255, 255)}

The keys are presented here with their ASCII code. For exaple the ASCII code for 
``k`` is 107. Colors are represented as tuples. The color black is represented as (0, 0, 0).

The event loop now becomes very simple. 
First we check if the event type is a KEYDOWN event.
If yes, we check if the event key is in the dictionary.
If yes, we look up the color which is associated with that key 
and set the background color to it::

    if event.type == KEYDOWN:
        if event.key in key_dict:
            background = key_dict[event.key]

Try to press the 8 specified keys to change the background color.

Change the window caption
-------------------------

The fonction ``pygame.display.set_caption(title)`` allows to change the caption (title) 
of the application window. We can add this to the event loop::

    if event.key in key_dict:
        background = key_dict[event.key]
        
        caption = 'background color = ' + str(background)
        pygame.display.set_caption(caption)

This will display the RGB value of the current background color in the window caption.

.. image:: intro5.png


Explore a simple ball game
--------------------------

To show what Pygame can do, here is a simple program 
that does a bouncing ball animation::

    import pygame
    from pygame.locals import *

    width = 640
    height = 320
    speed = [2, 2]
    GREEN = (150, 255, 150)
    running = True

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    ball = pygame.image.load("ball.gif")
    ballrect = ball.get_rect()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT: 
                running = False

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(GREEN)
        screen.blit(ball, ballrect)
        pygame.display.flip()

    pygame.quit()

.. image:: intro6.png

:download:`ball.gif<ball.gif>`

Try to understand what the program does. Then try to modify it's parameters.