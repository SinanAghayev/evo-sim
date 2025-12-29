MAX_MOVES = 400
pg_size = 250
c_count = 500
brainComplexity = 1
limit = 20

size = width, height = 1080, 800
black = 0, 0, 0
white = 255, 255, 255
h_start, v_start = 20, 20

c_size = 3
h_end, v_end = pg_size * c_size + h_start, pg_size * c_size + v_start

get_connection = False
fromFile = False
mutate = True
show, slow = True, False


playground = [[0 for i in range(pg_size)] for _ in range(pg_size)]
creatures = []
survivors = []
empty_squares = [(i, j) for i in range(pg_size) for j in range(pg_size)]
