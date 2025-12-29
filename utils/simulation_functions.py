import random
from data_types.constants import *
from data_types.creature import Creature
from data_types.connection import Connection
from functions.ui_functions import *


def chooseCoord():
    rnd = random.randint(0, len(empty_squares) - 1)
    x, y = empty_squares[rnd]
    empty_squares.pop(rnd)
    return x, y


def create():
    creatures = []
    ID = 0
    # TODO Not rewritten, may be (probably) buggy
    if fromFile:
        with open("best_new.txt", "r") as file:
            brains = [i.replace("\n", "").split("-") for i in file]
            for brain in brains:
                conn = []
                x, y = chooseCoord()
                c = Creature(x=x, y=y, newBrain=False)
                for i in brain:
                    connect = i.replace(",", "").split()
                    conn.append(
                        Connection(
                            int(connect[0]), int(connect[2]), float(connect[1]), c
                        )
                    )
                c.brain.addExistingConnectionsFromFile(conn)
                creatures.append(c)

    if len(survivors) != 0:
        for i in survivors:
            past_x, past_y = i.x, i.y
            i.x, i.y = chooseCoord()
            change_position(past_x, past_y, i.x, i.y, i.color)
            creatures.append(i)

        for i in range(c_count):
            if len(creatures) >= c_count:
                break
            if len(survivors) < 2:
                break

            x, y = chooseCoord()
            creature = Creature(x=x, y=y, ID=ID, newBrain=False)
            ID += 1

            c1 = survivors[random.randint(0, len(survivors) - 1)]
            c2 = survivors[random.randint(0, len(survivors) - 1)]
            conn = []

            if i < len(survivors):
                conn = survivors[i].get_brain().connections
            else:
                conn = (
                    c1.get_brain().get_random_half() + c2.get_brain().get_random_half()
                )

            creature.get_brain().addExistingConnections(conn)
            create_creature(creature)

    if len(creatures) < c_count:
        for _ in range(c_count - len(creatures)):
            x, y = chooseCoord()
            creature = Creature(x=x, y=y, ID=ID)
            create_creature(creature)
            ID += 1

    print(f"c count: {len(creatures)}")


def erase():
    survivors = []
    for creature in creatures.copy():
        delete_creature(creature)
        if creature.x < 50:
            survivors.append(creature)

    empty_squares = [(i, j) for i in range(pg_size) for j in range(pg_size)]
    print(f"survivors: {len(survivors)}")
    return survivors


# For radiation
def erase_one(t):
    for creature in creatures.copy():
        i = random.randint(1, 1000)
        if i != 1:
            continue
        if (creature.x < 125 and t < MAX_MOVES / 2) or (
            creature.x > 125 and t > MAX_MOVES / 2
        ):
            delete_creature(creature)


def mutation():
    for creature in creatures:
        mutation_rate = random.randint(1, c_count * 1000)
        if mutation_rate == 1:
            creature.get_brain().mutate()


def create_barrier():
    for i in range(10, pg_size - 10):
        playground[i][limit + 5] = 1
        draw_to_screen(i, limit + 5, black)


def moveNorth(a):
    if a.y > 0 and (playground[a.y - 1][a.x] != 1):
        change_position(a.x, a.y, a.x, a.y - 1, a.color)
        a.y -= 1


def moveSouth(a):
    if a.y < pg_size - 1 and (playground[a.y + 1][a.x] != 1):
        change_position(a.x, a.y, a.x, a.y + 1, a.color)
        a.y += 1


def moveWest(a):
    if a.x > 0 and (playground[a.y][a.x - 1] != 1):
        change_position(a.x, a.y, a.x - 1, a.y, a.color)
        a.x -= 1


def moveEast(a):
    if a.x < pg_size - 1 and (playground[a.y][a.x + 1] != 1):
        change_position(a.x, a.y, a.x + 1, a.y, a.color)
        a.x += 1


def move(c):
    direction = c.get_facing()
    # print(f"creature {creatures.index(c)} to {direction}")
    if direction == 0:
        moveWest(c)
    elif direction == 1:
        moveNorth(c)
    elif direction == 2:
        moveEast(c)
    elif direction == 3:
        moveSouth(c)


def change_position(x1, y1, x2, y2, color):
    playground[y1][x1] = 0
    playground[y2][x2] = 1

    draw_to_screen(x1, y1, white)
    draw_to_screen(x2, y2, color)


def create_creature(c):
    playground[c.y][c.x] = 1
    draw_to_screen(c.x, c.y, c.color)
    creatures.append(c)
    if (c.x, c.y) in empty_squares:
        empty_squares.remove((c.x, c.y))


def delete_creature(c):
    playground[c.y][c.x] = 0
    draw_to_screen(c.x, c.y, white)
    creatures.remove(c)
