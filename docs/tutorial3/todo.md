To do
=====

capture to current repository (8 May)
-------------------------------------

get the name of the calling class::

    name = type(self).__name__

save a file in the same folder of where it runs

    module = sys.modules['__main__']
    path = os.path.dirname(module.__file__)
    filename = path + '/' + name + '.png'
    pygame.image.save(Game.screen, filename)

Resize the display
------------------

When risizing the display the objects scale and get out of ratio. 
However the image captured stays the same.

Combine left and right cmd/alt/shift keys
-----------------------------------------

