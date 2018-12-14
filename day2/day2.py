from collections import namedtuple

INPUT_FILE = 'input.txt'

BoxBoy = namedtuple('BoxBoy', ['box1pos', 'box2pos', 'shared_chars'])
Char = namedtuple('Char', ['pos', 'char'])


def parse_input_file(fname):
    with open(fname, 'r') as file:
        contents = file.read().split()
    return contents


def has_n_same(string, n):
    """ return true if string contains a char that appears exactly x times """
    all_chars = {}
    for char in string:  # sum up count of each char
        all_chars.setdefault(char, 0)
        all_chars[char] += 1
    for char, count in all_chars.items():  # check how many appeared n times
        if count == n:
            return True
    return False


def get_checksum(boxlist):
    """ return product of boxes with 2 same chars and boxes with 3 same chars """
    twosames = threesames = 0
    for boxname in boxlist:
        if has_n_same(boxname, 2):
            twosames += 1
        if has_n_same(boxname, 3):
            threesames += 1
    return twosames * threesames


def find_shared_chars_of_neighbours(boxlist):
    """ return the string of shared characters between the correct boxes """
    for b1_pos, b1_name in enumerate(boxlist):
        for b2_name in boxlist[b1_pos:]:  # skip boxes that have been compared already
            shared_chars = []
            misses = 0
            for pos, char in enumerate(b1_name):
                if b2_name[pos] == char:  # hit, char is shared
                    shared_chars.append(char)
                else:  # miss
                    misses += 1
            if misses == 1:  # assume only looking for two boxes and return instantly
                return ''.join(shared_chars)


def main():
    warehouse_boxes = parse_input_file(INPUT_FILE)
    print('checksum:', get_checksum(warehouse_boxes))
    print('shared chars:', find_shared_chars_of_neighbours(warehouse_boxes))


if __name__ == '__main__':
    main()
