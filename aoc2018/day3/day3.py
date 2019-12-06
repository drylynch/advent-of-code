from collections import namedtuple

INPUT_FILE = 'input.txt'


def parse_claims_input(fname):
    """ return a list of ElfClaims from a file formatted as '#{id} @ {x},{y}: {width}x{height}\n' """
    ElfClaim = namedtuple('ElfClaim', ['id', 'x', 'y', 'width', 'height'])
    all_claims = []
    with open(fname, 'r') as file:
        contents = file.read().split('\n')
    for line in contents:
        line = line.strip()
        if line:  # ignore blank lines
            line = line.split(' ')  # ['#{id}', '@', '{x},{y}:', '{width}x{height}']
            cid = int(line[0][1:])  # ignore start hash
            cx, cy = line[2].split(',')
            cx = int(cx)
            cy = int(cy[:-1])  # cut off colon
            cw, ch = line[3].split('x')
            cw = int(cw)
            ch = int(ch)
            all_claims.append(ElfClaim(cid, cx, cy, cw, ch))

    return all_claims


def find_fabric_dimensions(claimlist):
    """ trawl through a list of claims and return a width and height of fabric big enough to fit all of them """
    cur_width = cur_height = 0
    for claim in claimlist:
        cur_width = max(cur_width, claim.x + claim.width)
        cur_height = max(cur_height, claim.y + claim.height)
    return cur_width, cur_height


def build_empty_array(width, height, blank):
    """ return an empty 2d array width x height filled with blank char, with some extra padding """
    array = []
    for _ in range(width):
        array.append([blank] * height)
    return array


def populate_fabric_array(fabric, claimlist, overlap_char):
    """ map each claim in claimlist to fabric array, with claim id in claimed space overlap_char and for overlapping claims """
    overlap_count = 0
    good_claims = set()
    for claim in claimlist:
        good_claims.add(claim.id)

    for claim in claimlist:
        for offset_x in range(claim.width):
            for offset_y in range(claim.height):
                x = claim.x + offset_x
                y = claim.y + offset_y

                if fabric[x][y] is None:  # free space, all cool
                    fabric[x][y] = claim.id
                else:  # not free!
                    if fabric[x][y] in good_claims:  # invalidate the claim already there
                        good_claims.remove(fabric[x][y])
                    if claim.id in good_claims:  # invalidate this claim
                        good_claims.remove(claim.id)
                    if fabric[x][y] != overlap_char:  # needs to be marked and counted
                        fabric[x][y] = overlap_char
                        overlap_count += 1

    return fabric, overlap_count, good_claims


def main():
    claimlist = parse_claims_input(INPUT_FILE)
    f_width, f_height = find_fabric_dimensions(claimlist)
    fabric = build_empty_array(f_width, f_height, None)
    fabric, overlap_count, good_claims = populate_fabric_array(fabric, claimlist, 'X')

    print('overlapped squares:', overlap_count)
    print('good claims:', good_claims)


if __name__ == '__main__':
    main()
