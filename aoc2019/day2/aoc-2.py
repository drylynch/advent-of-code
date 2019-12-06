from vm import VM


def test_pt1():
    vm = VM()
    print(vm.compute('1,9,10,3,2,3,11,0,99,30,40,50') == 3500)
    print(vm.compute('1,0,0,0,99') == 2)
    print(vm.compute('1,1,1,4,99,5,6,0,99') == 30)


def do_pt1():
    with open('input') as f:
        intcode = f.read()
    intcode = VM.sanitise_memory(intcode)
    intcode[1] = 12
    intcode[2] = 2
    vm = VM()
    print(vm.compute(intcode))


def do_pt2():
    with open('input') as f:
        clean_intcode_str = f.read()
    # intcode = VM.sanitise_memory(intcode)
    vm = VM()
    for i in range(0, 100):  # noun
        # print('trying noun = {0}, verb = '.format(i), end='')
        for j in range(0, 100):  # verb
            # print("{0}, ".format(j), end='')
            intcode = VM.sanitise_memory(clean_intcode_str)
            intcode[1] = i
            intcode[2] = j
            if vm.compute(intcode) == 19690720:
                print('found! noun: {0}, verb: {1}'.format(i, j))
                print('answer: 100 * noun + verb = {0}'.format(100 * i + j))
                break


if __name__ == '__main__':
    do_pt2()
