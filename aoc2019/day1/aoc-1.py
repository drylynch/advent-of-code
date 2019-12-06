import math


def calc_fuel_pt1(mass):
    return math.floor(mass / 3) - 2


def calc_fuel_pt2(mass):
    fuel_required = calc_fuel_pt1(mass)
    if fuel_required <= 0:
        return 0
    else:
        return fuel_required + calc_fuel_pt2(fuel_required)


def test_pt1():
    print(calc_fuel_pt1(12) == 2)
    print(calc_fuel_pt1(14) == 2)
    print(calc_fuel_pt1(1969) == 654)
    print(calc_fuel_pt1(100756) == 33583)


def test_pt2():
    print(calc_fuel_pt2(14))
    print(calc_fuel_pt2(1969))
    print(calc_fuel_pt2(100756))


def do_pt1():
    with open('input1.txt') as f:
        sum_fuel = 0
        for line in f:
            sum_fuel += calc_fuel_pt1(int(line))
        print('answer:', sum_fuel)


def do_pt2():
    with open('input1.txt') as f:
        sum_fuel = 0
        for line in f:
            sum_fuel += calc_fuel_pt2(int(line))
        print('answer:', sum_fuel)


if __name__ == '__main__':
    do_pt2()
