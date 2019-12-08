class SIFImg:
    def __init__(self):
        """ Space Image Format (SIF) image """
        self.width = None
        self.height = None
        self.raw_layers = None
        self.image = None
        self.palette = {'0': '#',  # black
                        '1': ' ',  # white
                        '2': '.'}  # transparent

    def load(self, raw_data, width, height):
        """ load image data, width and height """
        self.width = width
        self.height = height
        self.raw_layers = self._parse_raw_data(raw_data)
        self._collapse()

    def compute_checksum(self):
        """ return int checksum of img """
        checksum_layers = {}
        for i, layer in enumerate(self.raw_layers):
            count0 = count1 = count2 = 0
            for item in layer:
                if item == '0':
                    count0 += 1
                elif item == '1':
                    count1 += 1
                elif item == '2':
                    count2 += 1
            checksum_layers[count0] = (count1, count2)
        chk = checksum_layers[min(checksum_layers)]
        return chk[0] * chk[1]

    def set_palette(self, black, white, transparent):
        """ set characters to print for each colour """
        self.palette = {'0': black,
                        '1': white,
                        '2': transparent}

    def print(self):
        """ print SIF image """
        for i, layer in enumerate(self.image):
            pixel = (p for p in layer)
            for _ in range(self.height):
                for _ in range(self.width):
                    p = self.palette.get(next(pixel))
                    print(p, end=' ')
                print()
            print()

    def _parse_raw_data(self, raw_data):
        """ return array of raw img layers from raw data """
        layers = []
        pixels = (p for p in raw_data)
        while True:  # continue until no more img data
            try:
                layer = []
                for x in range(self.width * self.height):
                    layer.append(next(pixels))
                layers.append(layer)
            except StopIteration:
                break
        return layers

    def _collapse(self):
        """ return single layer combo of all img layers """
        final_layer = [None] * (self.width * self.height)
        for layer in self.raw_layers:
            for position, pixel in enumerate(layer):
                if final_layer[position] is None and pixel != '2':
                    final_layer[position] = pixel
        self.image = self._parse_raw_data(final_layer)


def test_pt1():
    img = SIFImg()
    img.load('121021021022', *(3, 2))
    print(img.compute_checksum() == 6)


def do_pt1():
    with open('input') as f:
        data = f.read()
    size = (25, 6)
    img = SIFImg()
    img.load(data, *size)
    print(img.compute_checksum())


def test_pt2():
    """ correct result: B W
                        W B """
    img = SIFImg()
    img.load('0222112222120000', *(2, 2))
    img.set_palette(*('B', 'W', 'T'))
    img.print()


def do_pt2():
    with open('input') as f:
        data = f.read()
    size = (25, 6)
    img = SIFImg()
    img.load(data, *size)
    img.set_palette(*('     ', 'ZFLBY', '.....'))  # invert black and white for visibility
    img.print()


if __name__ == '__main__':
    do_pt2()
