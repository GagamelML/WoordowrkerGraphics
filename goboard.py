import drawsvg as draw

path = 'D:\Eigene Dateien\Pictures\Laser\Go13noSQ.svg'

grid = 13
dotsize = .11
square = False
scale = 100

class Board:

    """
    Parameters
    ----------
    grid: int
        grid of the board. Supported: 9, 13 or 19 (Default is 9)
    dotsize: float
        Size of the dots in fraction of one line spacing. 0 to remove dots. Default: 0
    square: bool
        Format of the board. "True" for square. "False" will multiply width with 14/15 to account for perspective (original Japanese style)
    scale: int
        Scaling factor. Num of px per line spacing in x
    """
    def __init__(self, grid: int = 9, dotsize: float = 0.0, square: bool = True, scale: int = 100):
        self.grid = grid
        self.dotsize = dotsize
        self.square = square

        self.scaling_x = scale
        if square:
            self.scaling_y = scale
        else:
            self.scaling_y = scale * 14 / 15

        # relative pos of dots
        if self.grid == 9:
            self.dot_pos = [[2,2], [2,6],
                            [4,4],
                            [6,2], [6,6]]
        elif self.grid == 13:
            self.dot_pos = [[3,3], [3,9], [9,3], [9,9], [6,6]]
        else:
            self.dotlines = []
            t = []
            for i in [3, 9, 15]:
                for k in [3, 9, 15]:
                    t.append([i, k])
            self.dot_pos = t

    def get_holepos_in_line(self, linenum: int):
        h = []
        for dot in self.dot_pos:
            if dot[0] == linenum:
                h.append(dot[1])
        return h

    def get_line_parts(self, linenum: int, smallside: bool = False):
        ds = self.dotsize
        if smallside:
            ds = ds * 15 / 14
        h = self.get_holepos_in_line(linenum)
        if ds != 0 and len(h) != 0:
            parts = [[0, h[0]-ds]]
            for k in range(len(h)-1):
                parts.append([h[k]+ds, h[k+1]-ds])
            parts.append([h[len(h)-1]+ds, self.grid-1])
        else:
            parts = [[0, self.grid-1]]
        return parts

    def set_scaling(self, s:float):
        self.scaling_x = s
        if self.square:
            self.scaling_y = s
        else:
            self.scaling_y = s * 14 / 15

    def draw_board(self, d: draw.Drawing):
        sx = self.scaling_x
        sy = self.scaling_y
        for l in range(self.grid):
            x = l * sx
            y = l * sy
            parts_x = self.get_line_parts(l)
            parts_y = self.get_line_parts(l, smallside=not self.square)
            for p in parts:
                # todo: this is an incoplete change. parts is now spit into party_y nd parts_x,
                # the following two lines need to change accordingly
                # for loop needs to be 2 for loops
                d.append(draw.Line(p[0] * sx, y, p[1] * sx, y, stroke='black'))
                d.append(draw.Line(x, p[0] * sy, x, p[1] * sy, stroke='black'))

        if self.dotsize != 0:
            for dotpos in self.dot_pos:
                d.append(draw.Circle(dotpos[0]*sx, dotpos[1]*sy, self.dotsize*sx, stroke='black'))
        return d


board = Board(grid=grid, dotsize=dotsize, square=square, scale=scale)
d = draw.Drawing(board.scaling_x * grid, board.scaling_y * grid, origin=[0, 0])
board.draw_board(d)
d.save_svg(path)

