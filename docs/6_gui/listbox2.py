"""Display a ListBox multiple selections."""
from app import *

atts = dir()

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='ListBox', bg=Color('beige'))
        ListBox(['Charlie', 'Daniel', 'Tim', 'Jack'], cmd='print(self.item)')

        cities = ['Amsterdam', 'Berlin', 'Cardiff', 'Dublin', 'Edinbourgh', 'Fargo', 'Greenwich', 
                'Harrington', 'Melbourne', 'New York', 'Oslo', 'Paris']
        ListBox(cities, dir=(1, 0))
        ListBox(atts, width=300, align=1)

if __name__ == '__main__':
    Demo().run()