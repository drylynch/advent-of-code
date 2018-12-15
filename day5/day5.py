INPUT_FILE = 'input.txt'


def slice_string(string, from_here, to_here):
    """ hiyaa """
    return string[:from_here] + string[to_here + 1:]


def are_inverse(char, other):
    """ true if char is inverted case from other, eg aA, Aa """
    if char.isupper() and other.islower() and char == other.upper():  # Aa
        return True
    elif char.islower() and other.isupper() and char == other.lower():  # aA
        return True
    return False


def fully_collapse(string):
    """ fully collapses a string duh """
    pos = 0
    while pos != len(string) - 1:
        char = string[pos]
        right = string[pos+1]
        if are_inverse(char, right):
            string = slice_string(string, pos, pos + 1)
            if pos != 0:
                pos -= 1  # move back to allow checking the prev char with its new right neighbour
        else:
            pos += 1
    return string


def cut_all(killchar, string):
    """ removes all instances of char from string, ignoring case """
    string = string.replace(killchar.lower(), '')
    string = string.replace(killchar.upper(), '')
    return string


def main():
    with open(INPUT_FILE, 'r') as file:
        string = file.read().strip()

    # part 1
    string = fully_collapse(string)
    print('string:', string)
    print('len:', len(string))

    # part 2
    new_lengths = []
    for char in 'abcdefghijlmnopqrstuvwxyz':
        new_lengths.append(len(fully_collapse(cut_all(char, string))))
    print('best length:', min(new_lengths))


if __name__ == '__main__':
    main()
