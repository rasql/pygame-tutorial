## PyGame and Tiled Platformer Demo
An object oriented demo of a platformer game loading a map from the [Tiled Map Editor](http://www.mapeditor.org/) using [PyGame](http://pygame.org/news.html) and [PyTMX](http://pytmx.readthedocs.org/en/latest/). Graphics from the HTML5 game [Biolab Disaster](http://playbiolab.com/).

### Running
Just download and run `main.py`, dependencies are [Python 3.4](https://www.python.org/), [PyGame](http://pygame.org/news.html), and [PyTMX](http://pytmx.readthedocs.org/en/latest/).

### Documentation
The basic structure of the game and how it loads the map is as follows..
* A basic game class that has a list of level objects
* The level objects are loaded with a TMX map file, using PyTMX
* Levels contain a list of layer objects, one for each layer in the map
* Each layer has a list of tiles, that is actually a PyGame sprite group

The tile objects are created in the initialiation of each layer. A player is added through the player class and collision is easily detected by checking the sprite collision of whatever layer your map uses for collision.
