COM = 'COM'  # universal center of mass: orbits nothing, is indirectly orbited by everything


def parse_orbit_map(orbit_map):
    """ return dict of all (orbiter: orbitee) """
    o = {}
    orbit_map = orbit_map.split('\n')
    for pair in orbit_map:
        orbitee, orbiter = pair.split(')')
        o[orbiter] = orbitee
    return o


def count_total_orbits_for_orbiter(orbiter, o):
    """ return total number of orbits, direct and indirect, between this orbiter and the COM """
    if o[orbiter] == COM:
        return 1
    else:
        return 1 + count_total_orbits_for_orbiter(o[orbiter], o)


def count_total_orbits_in_orbit_map(orbit_map):
    """ return number of direct and indirect orbits in entire orbit map """
    sum_orbits = 0
    for each in orbit_map.keys():  # for each orbiter
        sum_orbits += count_total_orbits_for_orbiter(each, orbit_map)
    return sum_orbits


def create_rootpath(startnode, endnode, orbit_map):
    """ return list of nodes between start and end nodes in orbit map """
    rootpath = [startnode]  # include start
    current = startnode
    while current != endnode:
        current = orbit_map[current]
        rootpath.append(current)
    return rootpath


def find_earliest_common_node(n1, n2, orbit_map):
    """ return name of first node that is ancestor to both n1 and n2 """
    rootpath_n1 = create_rootpath(n1, COM, orbit_map)
    rootpath_n2 = create_rootpath(n2, COM, orbit_map)
    for n1 in rootpath_n1:
        for n2 in rootpath_n2:
            if n1 == n2:
                return n1  # first node encountered is their closest shared ancestor node


def minimum_jumps_from(n1, n2, orbit_map):
    """ return minimum jumps needed to get from n1 to n2 in orbit map """
    common_ancestor = find_earliest_common_node(n1, n2, orbit_map)
    jumps_n1_to_common = len(create_rootpath(n1, common_ancestor, orbit_map)) - 1  # number of vertices = number of nodes - 1
    jumps_n2_to_common = len(create_rootpath(n2, common_ancestor, orbit_map)) - 1
    return jumps_n1_to_common + jumps_n2_to_common


def do_pt1():
    with open('input') as f:
        orbit_map = f.read()
    orbit_map = parse_orbit_map(orbit_map)
    print(count_total_orbits_in_orbit_map(orbit_map))


def test_pt1():
    orbit_map = parse_orbit_map("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L")
    print(count_total_orbits_in_orbit_map(orbit_map) == 42)


def do_pt2():
    with open('input') as f:
        orbit_map = f.read()
    orbit_map = parse_orbit_map(orbit_map)
    start = orbit_map.get('YOU')
    end = orbit_map.get('SAN')
    print(minimum_jumps_from(start, end, orbit_map))


def test_pt2():
    orbit_map = parse_orbit_map("COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN")
    start = orbit_map.get('YOU')
    end = orbit_map.get('SAN')
    print(minimum_jumps_from(start, end, orbit_map) == 4)


if __name__ == '__main__':
    do_pt2()
