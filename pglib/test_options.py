"""Quick test of class properties."""

class MyClass:
    pos=(10, 10)
    # color = Color('beige')
    title = 'MyClass'

    def __init__(self, **options):

        print('\n', '=' * 30)
        print(self)

        self.pos = (0, 0)
        self.set_options(options)
        self.__dict__.update(options)

        print('-- instance options', '-'*30)
        self.print_dict(self.__dict__)
        print('-- class options', '-'*30)
        self.print_dict(self.__class__.__dict__)

    def print_dict(self, d):
        for k, v in d.items():
            if not k.startswith('_'):
                print(k, v, sep='\t')

    def set_options(self, options):
        for k, v in options.items():
            if k in self.__dict__:
                self.__dict__[k] = v
            else:
                msg = "option '{}' does not exist'".format(k)
                print(msg)
        

m = MyClass()
m1 = MyClass(x=20) # non-existing option
m2 = MyClass(pos=(100, 100)) # existing option