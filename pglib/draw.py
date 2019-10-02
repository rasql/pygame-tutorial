import pygame
from .app import *

class Text(Node):
    """Create a text object which knows how to draw itself."""

    def __init__(self, text, **options):
        """Instantiate and render the text object."""
        super().__init__(**options)

        self.str = text
        self.fontsize = 72
        self.fontcolor = Color('black')
        self.render()

        # Append the node to the current window
        App.scene.nodes.append(self)

    def render(self):
        """Render the string and create a surface object."""
        self.font = pygame.font.Font(None, self.fontsize)
        self.text = self.font.render(self.str, True, self.fontcolor)
        self.rect = self.text.get_rect()
        self.rect.topleft = self.pos
        self.size = self.rect.size
        Node.options['size'] = self.size

    def draw(self):
        """Draw the text surface on the screen."""
        App.screen.blit(self.text, self.pos)
        Node.draw(self)


class Rectangle(Node):
    """Draw a rectangle on the screen."""

    def __init__(self, **options):
        super().__init__(**options)

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, self.d)
        Node.draw(self)


class Ellipse(Node):
    """Draw an ellipse on the screen."""

    def __init__(self, **options):
        super().__init__(**options)

    def draw(self):
        pygame.draw.ellipse(App.screen, self.color, self.rect, self.d)
        Node.draw(self)


class Button:
    pass



