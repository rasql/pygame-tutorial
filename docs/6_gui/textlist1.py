"""Template for making applications."""

from app import *

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='TextList')
        TextList(['Charlie', 'Daniel', 'Tim', 'Jack'], cmd='print(self.item)')

        cities = ['Amsterdam', 'Berlin', 'Cardiff', 'Dublin', 'Edinbourgh', 'Fargo', 'Greenwich', 'Harrington', 'Melbourne']
        TextList(cities, dir=(1, 0))
        
if __name__ == '__main__':
    Demo().run()