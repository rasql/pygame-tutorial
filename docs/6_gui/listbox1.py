"""Display a ListBox with left/center/right alignement."""
from app import *

atts = dir()

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='ListBox', bg=Color('beige'))
        ListBox(['Charlie', 'Daniel', 'Tim', 'Jack'], cmd='print(self.item)')

        cities = ['Amsterdam', 'Berlin', 'Cardiff', 'Dublin', 'Edinbourgh', 'Fargo', 'Greenwich', 
            'Harrington', 'Melbourne', 'New York', 'Oslo', 'Paris']    
        ListBox(cities, dir=(1, 0), wrap=True, align=1)
        ListBox(atts, width=350, align=2, wrap=False)
        
if __name__ == '__main__':
    Demo().run()