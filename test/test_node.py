from pg_app import *

s0 = Scene()
n0 = Node()
n1 = Node()
n2 = Node()

def test_node():
    assert App.scenes == [s0]
    assert App.scene == s0
    assert App.scene.nodes == [n0, n1, n2]

if __name__ == '__main__':
    print('test')