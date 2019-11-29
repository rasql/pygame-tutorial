# class method

class A:
    att = 'class attr'

    def __init__(self, arg, *args, **kwargs):
        self.att = 'instance attr'
        self.att2 = A.att
        print('Create instance...')
        print('type(self.__dict__) =', type(self.__dict__))

    @classmethod
    def update_options(cls, options):
        print('Update class options...')
        print('type(cls.__dict__) =', type(cls.__dict__))
        cls.att = 'updated' 

def print_info(obj):
    print('='*10, obj)
    for key in obj.__dict__:
        if not key.startswith('__'):
            print(f'{key} = {obj.__dict__[key]}')

a = A('aa')

print_info(A)
a.update_options({'key':'value', 1:100})
print_info(A)
print_info(a)
a2 = A('aa2')
print_info(a2)
