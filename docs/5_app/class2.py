# Initialize instance options from class options, update class options from instance 

class A:
    """Class A with options and serial id."""
    options0 = {
        'id': 0,
        'opt1': 1,
    }
    options = options0.copy()
    stack = []

    @classmethod
    def reset_options(cls):
        print(f'> reset class {cls.__name__} options')
        cls.options = cls.options0.copy()

    @staticmethod
    def increment_id():
        A.options['id'] += 1 

    def __init__(self, once=False, **options):
        self.set_options(A, once, options)
        self.increment_id()

    def set_options(self, cls, once, options):
        #print(f'set class {cls.__name__} options')
        if once:
            self.__dict__.update(cls.options)
            self.__dict__.update(options)
        else:
            for key in options:
                if key in cls.options:
                    cls.options[key] = options[key]
            self.__dict__.update(cls.options)

    def info(self):
        print('---', self, self.__dict__)
        # for key in self.__dict__:
        #     if not key.startswith('__'):
        #         print(f'{key} = {self.__dict__[key]}')
        return self  # returns itself to allow chaining

    def __str__(self):
        return self.__class__.__name__

class B(A):
    options0 = {
        'opt2':  2,
    }
    options = options0.copy()

    def __init__(self, once=False, **options):
        super().__init__(once, **options)
        self.set_options(B, once, options)

class C(B):
    options0 = {
        'opt3':  3,
    }
    options = options0.copy()

    def __init__(self, once=False, **options):
        super().__init__(once, **options)
        self.set_options(C, once, options)

A().info()
A(opt1=9, once=True).info()
A().info().reset_options()
A().info()
B(opt1=9, opt2=9, once=True).info()
B().info()
C().info()
C(opt2=9, opt3=9).info()
C().info()