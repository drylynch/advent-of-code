import intcomputer


def do():
    with open('input') as f:
        instructions = f.read()
    vm = intcomputer.VM()
    vm.compute(instructions)


def test_pt2_eq_lt():
    vm = intcomputer.VM()
    vm.compute('3,9,8,9,10,9,4,9,99,-1,8')  # if input == 8, print 1, else print 0 (positional)
    vm.compute('3,9,7,9,10,9,4,9,99,-1,8')  # if input < 8, print 1, else print 0 (positional)
    vm.compute('3,3,1108,-1,8,3,4,3,99')  # if input == 8, print 1, else print 0 (immediate)
    vm.compute('3,3,1107,-1,8,3,4,3,99')  # if input < 8, print 1, else print 0 (immediate)
    # inputs: 8888 -> 1010, 7777 -> 0101


def test_pt2_jump():
    vm = intcomputer.VM()
    vm.compute('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9')  # if input == 0, print 0, else print 1
    vm.compute('3,3,1105,-1,9,1101,0,0,12,4,12,99,1')  # if input == 0, print 0, else print 1


def test_pt2_all():
    vm = intcomputer.VM()
    # input < 8, print 999. input == 8, print 1000. input > 8, print 1001
    vm.compute('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99')


if __name__ == '__main__':
    do()
