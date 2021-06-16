Breakout
========

Breakout is an arcade game developed and published by Atari and released in 1976.

Breakout begins with eight rows of bricks, with each two rows a different color. 
The color order from the bottom up is 
- yellow, 
- green, 
- orange and 
- red. 

Using a single ball, the player must knock down as many bricks as possible by using the walls and/or the paddle below to ricochet the ball against the bricks and eliminate them. 

If the player's paddle misses the ball's rebound, they will lose a turn. 
The player has three turns to try to clear two screens of bricks. 
Yellow bricks earn one point each, green bricks earn three points, orange bricks earn five points and the top-level red bricks score seven points each. 
The paddle shrinks to one-half its size after the ball has broken through the red row and hit the upper wall. 

Ball speed increases at specific intervals: after four hits, after twelve hits, and after making contact with the orange and red rows.
The highest score achievable for one player is 896; this is done by eliminating two screens of bricks worth 448 points per screen. 

.. image:: https://upload.wikimedia.org/wikipedia/en/c/cd/Breakout_game_screenshot.png

Making an app
-------------

The first step is to create a frame work which creates a window

.. image:: pong1.png

.. literalinclude:: app.py
   :lines: 3-

:download:`app.py<app.py>`