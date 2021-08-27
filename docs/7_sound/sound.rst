Playing sound
=============

Making sounds
-------------

The ``pygame.mixer`` module allows to play compressed OGG files or uncompressed WAV files.

This checks the initialization parameters and prints the number of channels available.
It opens a sound object and plays it::

    print('init =', pygame.mixer.get_init())
    print('channels =', pygame.mixer.get_num_channels())
    App.snd = pygame.mixer.Sound('5_app/rpgaudio.ogg')
    App.snd.play()
    print('length =', App.snd.get_length())

Writes this to the console::

    init = (22050, -16, 2)
    channels = 8
    length = 28.437868118286133

Here is a code example:

.. literalinclude:: sound1.py

Which produces the following result.

.. image:: sound1.png
