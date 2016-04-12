import math

class Hex:
    def __init__(self, c, r):
        self._size = 17;
        self.c = c;
        self.r = r;
        self._cube = self.even_r_to_cube(c,r)
        height = self._size * 2;
        width = math.sqrt(3) / 2 * height
        self._x = self._size + (c + 1) * width - (r % 2) * width / 2
        self._y = self._size + 1 / 2 * height + (r + 1) * (height * 3 / 4)
        self._corners = self._gen_corners()

    def even_r_to_cube(self, col, row):
        x = col - (row + (row & 1)) / 2
        z = row
        y = -x - z
        return (x,y,z)

    def cube_to_even_r(self,cube):
        x,y,z = cube
        col = x + (z + (z & 1)) / 2
        row = z
        return col,row

    def get_neighbours(self):
        directions = ((1, -1, 0),(1, 0, -1),(0, 1, -1),
                      (-1, 1, 0),(-1, 0, 1),(0, -1, 1))
        cube_neighs = []
        for dir in directions:
            cube_neighs.append(map(sum, zip(dir,self._cube)))
        neighs = []
        for cn in cube_neighs:
            neighs.append(self.cube_to_even_r(cn))
        return neighs


    def get_key(self):
        return self.c, self.r

    def r_get_center(self):
        return (self._x,self._y)

    def r_get_corners(self):
        return self._corners;

    def in_hex(self, x, y):
        return abs(self._x - x) < self._size and\
               abs(self._y - y) < self._size

    def _hex_corner(self, i):
        angle_deg = 60 * i + 30
        angle_rad = math.pi / 180 * angle_deg
        return dict(x=(self._x + self._size * math.cos(angle_rad)), y=(self._y + self._size * math.sin(angle_rad)))

    def _gen_corners(self):
        corners = []
        for i in range(6):
            corners.append(self._hex_corner(i))
        return corners
