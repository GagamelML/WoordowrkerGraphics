import turtle as tt
import numpy as np

windowmax_y = 666
windowmax_x =1200
skip_double = False  # if this is true, the last strip of the base segment will not be mirrored in the following segment
defined_dimension = 'smallest' #C an be 'smallest' (for smallest strip), 'biggest' (for biggest strp) or 'total_x' or 'total_y' for total board dimensions
defined_value = 0.5 # Value that the defined dimension should have. Will calculate the other 3 parameters

boardsize_x = 500 # maximum size of board
x_start = 30        # width of first stripe
x_sections = 2      # number of mirror-symmetric sections
n_max_x = 7
# max number of strips within one inversion section
def funct_x(width, pos, n):
    return width*0.6


y_same = True   # if true ignore following parameters
boardsize_y = 500
y_start = 30
y_sections = 2
n_max_y = 4
def funct_y(width, pos, n):
    return width*0.6


def calc_points(start, function, size, inversions, n_max, skip_middle):
    #creates an array positions where every step is te size of the previous step multiplied by a factor.
    #inverts this process a number of times, inverting the factor. Total distance will be smaller than size.
    section_size = size/inversions
    total = start
    width = start
    widthdummy = np.zeros(1, dtype=float)
    n = 0
    #create array of line widths for one inversion section
    while (n < n_max):
        widthdummy = np.append(widthdummy, width)
        width = function(width, total, n)
        total = total + width
        n = n+1
    pointbase = np.delete(widthdummy, 0)
    #create array of all starting points over all inversion sections
    points = np.zeros(1, dtype=float)
    pos = 0

    if skip_middle:
        s = 1
        pos = pos + start
        points = np.append(points, pos)
    else:
        s = 0

    for num_inv in range(1, inversions+1):
        if num_inv % 2 == 1:
            for k in range(s, len(pointbase), +1):
                pos = pos + pointbase[k]
                points = np.append(points, pos)
        if num_inv % 2 == 0:
            for k in range(len(pointbase)-1-s, -1, -1):
                pos = pos + pointbase[k]
                points = np.append(points, pos)
    return [points, pos, min(pointbase), max(pointbase)]

# this is hopelessly outdated
def draw_lines(starts, direction, dist):
    # will draw parallel lines in direction (x or y) of length dist starting from all positions in starts
    t = tt.Pen()
    t.speed(8)
    if direction == 'x':
        for i in range(len(starts)):
            t.up()
            t.goto(starts[i], 0)
            t.seth(90)
            t.down()
            t.forward(dist)
    if direction == 'y':
        for i in range(len(starts)):
            t.up()
            t.goto(0, starts[i])
            t.seth(0)
            t.down()
            t.forward(dist)


def color_fields(points_x, points_y):

    #set up screen nd turtle
    max_x=max(points_x)
    max_y=max(points_y)
    max_coord = max(max_x, max_y)
    ratio = max(points_y)/max(points_x)

    if (windowmax_x/max_x) < (windowmax_y/max_y):
        win_width = windowmax_x
        win_height = windowmax_x*ratio
    else:
        win_height = windowmax_y
        win_width = windowmax_y/ratio
    window = tt.Screen()
    window.setup(width=win_width, height=win_height)
    tt.setworldcoordinates(-0.1*max_x, -0.1*max_y, 1.1*max_x, 1.1*max_y)
    t = tt.Pen()
    t.speed(0)

    #drawing stats here
    for x in range(len(points_x)-1):
        a = x % 2
        for y in range(len(points_y)-1):
            t.penup()
            t.goto(points_x[x], points_y[y])
            t.pendown()
            if a == 1:
                t.fillcolor('white')
                a = 0
            else:
                t.fillcolor('black')
                a = 1
            t.begin_fill()
            t.goto(points_x[x], points_y[y+1])
            t.goto(points_x[x+1], points_y[y+1])
            t.goto(points_x[x+1], points_y[y])
            t.goto(points_x[x], points_y[y])
            t.end_fill()

def calc_stats(def_dim, def_val, min_x, max_x, total_x, min_y, max_y, total_y):

    return


arrangement_x = calc_points(x_start, funct_x, boardsize_x, x_sections, n_max_x, skip_double)
if y_same:
    arrangement_y = arrangement_x
else:
    arrangement_y = calc_points(y_start, funct_y, boardsize_y, y_sections, n_max_y, skip_double)

# draw_lines(points_x, 'x', max_y)
# draw_lines(points_y, 'y', max_x)
color_fields(arrangement_x[0], arrangement_y[0])

# calculate some rations and thicknesses

tt.done()


