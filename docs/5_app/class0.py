# name space demo
name = 'global name'

class Class:
    name = 'class name'

    def __init__(self):
        self.name = 'inst name'
    
    def func1(self):
        return name
    
    def func2(self):
        return self.name
    
    def func3(self):
        name = 'local name'
        return name

    @staticmethod
    def stat_meth():
        return name

    @classmethod
    def cls_meth(cls):
        return name

    @classmethod
    def cls_meth2(cls):
        return cls.name

inst = Class()

print('name', name)
print('Class', Class.name)
print('inst', inst.name)
print('func1', inst.func1())
print('func2', inst.func2())
print('func3', inst.func3())
print('stat_meth', inst.stat_meth())
print('cls_meth', inst.cls_meth())
print('cls_meth2', inst.cls_meth2())



