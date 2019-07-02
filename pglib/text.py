class Text:
    pass

class Multitext:
    def __init__(self, text):
        self.text = text
        self.images = []
        self.rects = []

    def render_words(self):
        pass


if __name__ == '__main__':

    text = 'this is a \nMULTI-LINE text.' 
    
    a = text.split()
    print(a)
