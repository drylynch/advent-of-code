from collections import namedtuple

INPUT_FILE = 'input.txt'
Dude = namedtuple('Dude', ['op', 'num'])


def open_and_parse_input(alldudes_fname):
    """ split all-in-one chunky dudes into list of individual dude tuples (op, num) """
    with open(alldudes_fname, 'r') as file:
        whole_file = file.read().split()
    outdudes = []
    for line in whole_file:
        outdudes.append(Dude(line[0], int(line[1:])))
    return outdudes


def get_total(dudelist):
    """ sum up all numbers in a dudelist """
    total = 0
    for dude in dudelist:
        total = rolling_sum(total, dude)
    return total


def rolling_sum(cur_sum, dude):
    """ add a dude to the current sum """
    if dude.op == '+':
        cur_sum += dude.num
    else:
        cur_sum -= dude.num
    return cur_sum


def get_first_twicer(dudelist):
    """ print first occurrence of a duplicate total """
    all_totals = set()
    cur_total = 0
    while True:
        for dude in dudelist:
            cur_total = rolling_sum(cur_total, dude)
            if cur_total in all_totals:
                return cur_total
            else:
                all_totals.add(cur_total)


def main():
    dudelist = open_and_parse_input(INPUT_FILE)
    # print(get_total(dudelist))
    print(get_first_twicer(dudelist))


if __name__ == '__main__':
    main()
