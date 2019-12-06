START = 347312  # range of possible passwords
END = 805915


def group_same(stuff):
    """ return 2d list of adjacent same items, eg 122333 -> [[1], [2,2], [3,3,3]] """
    last = None
    accumulator = []
    groups = []
    for i in range(len(stuff)):
        item = stuff[i]
        if item == last or last is None:  # same or first
            accumulator.append(item)
        else:  # new item, split
            groups.append(accumulator)
            accumulator = [item]
        last = item
    groups.append(accumulator)  # add the last group
    return groups


def has_same_adjacent(stuff):
    """ true if any two adjacent digits in stuff are the same, eg [6, 2, 2, 3] """
    same_adjacent = False
    for i in range(len(stuff) - 1):  # len -1 to avoid overshooting end of list
        if stuff[i] == stuff[i + 1]:
            same_adjacent = True
            break
    return same_adjacent


def has_strict_double(stuff):
    """ true if there is at least one double item not in a larger group """
    has_clean_double = False
    for g in group_same(stuff):
        if len(g) == 2:
            has_clean_double = True
            break
    return has_clean_double


def is_always_increasing(stuff):
    """ true if all items >= their left neighbour, eg [2, 5, 7, 9, 9] """
    always_increasing = True
    for i in range(len(stuff) - 1):
        if stuff[i] > stuff[i + 1]:
            always_increasing = False
            break
    return always_increasing


def is_good_password_pt1(p):
    p_list = [x for x in str(p)]
    return is_always_increasing(p_list) and has_same_adjacent(p_list)


def is_good_password_pt2(p):
    p_list = [x for x in str(p)]
    return is_always_increasing(p_list) and has_strict_double(p_list)


def do_pt1():
    good_password_count = 0
    for num in range(START, END + 1):  # start to end inclusive
        if is_good_password_pt1(num):
            good_password_count += 1
    print(good_password_count)


def do_pt2():
    good_password_count = 0
    for num in range(START, END + 1):
        if is_good_password_pt2(num):
            good_password_count += 1
    print(good_password_count)


def test_pt1():
    print(is_good_password_pt1(111111) == True)
    print(is_good_password_pt1(223450) == False)
    print(is_good_password_pt1(123789) == False)


def test_pt2():
    print(is_good_password_pt2(112233) == True)
    print(is_good_password_pt2(123444) == False)
    print(is_good_password_pt2(111122) == True)
    print(is_good_password_pt2(666777) == False)


if __name__ == '__main__':
    do_pt2()
