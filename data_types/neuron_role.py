from enum import Enum
from data_types.enums import Direction, Turn
import data_types.constants as constants


class NeuronRole(str, Enum):
    # ===== INPUT =====
    AGE = "age"
    X_COORD = "x_coord"
    Y_COORD = "y_coord"
    DIST_TO_WEST = "dist_to_west"
    DIST_TO_EAST = "dist_to_east"
    DIST_TO_NORTH = "dist_to_north"
    DIST_TO_SOUTH = "dist_to_south"

    # ===== OUTPUT =====
    MOVE_WEST = "move_west"
    MOVE_NORTH = "move_north"
    MOVE_EAST = "move_east"
    MOVE_SOUTH = "move_south"
    MOVE_LEFT = "move_left"
    MOVE_FORWARD = "move_forward"
    MOVE_RIGHT = "move_right"
    MOVE_BACKWARD = "move_backward"
    MOVE_RANDOM = "move_random"
    NOTHING = "nothing"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"

    # ===== INTERNAL =====
    INTERNAL_0 = "internal_0"
    INTERNAL_1 = "internal_1"
    INTERNAL_2 = "internal_2"

    @property
    def is_input(self) -> bool:
        return self in {
            NeuronRole.AGE,
            NeuronRole.X_COORD,
            NeuronRole.Y_COORD,
            NeuronRole.DIST_TO_WEST,
            NeuronRole.DIST_TO_EAST,
            NeuronRole.DIST_TO_NORTH,
            NeuronRole.DIST_TO_SOUTH,
        }

    @property
    def is_output(self) -> bool:
        return self in {
            NeuronRole.MOVE_WEST,
            NeuronRole.MOVE_NORTH,
            NeuronRole.MOVE_EAST,
            NeuronRole.MOVE_SOUTH,
            NeuronRole.MOVE_LEFT,
            NeuronRole.MOVE_FORWARD,
            NeuronRole.MOVE_RIGHT,
            NeuronRole.MOVE_BACKWARD,
            NeuronRole.MOVE_RANDOM,
            NeuronRole.NOTHING,
            NeuronRole.TURN_LEFT,
            NeuronRole.TURN_RIGHT,
        }

    @property
    def is_internal(self) -> bool:
        return self.name.startswith("INTERNAL_")

    # ---------- INPUT BEHAVIOR ----------
    def read_value(self, creature) -> float:
        match self:
            case NeuronRole.AGE:
                return creature.get_age() / constants.MAX_MOVES
            case NeuronRole.X_COORD:
                return creature.x / constants.GRID_SIZE
            case NeuronRole.Y_COORD:
                return creature.y / constants.GRID_SIZE
            case NeuronRole.DIST_TO_WEST:
                return (
                    creature.distance_to_direction(Direction.WEST) / constants.GRID_SIZE
                )
            case NeuronRole.DIST_TO_EAST:
                return (
                    creature.distance_to_direction(Direction.EAST) / constants.GRID_SIZE
                )
            case NeuronRole.DIST_TO_NORTH:
                return (
                    creature.distance_to_direction(Direction.NORTH)
                    / constants.GRID_SIZE
                )
            case NeuronRole.DIST_TO_SOUTH:
                return (
                    creature.distance_to_direction(Direction.SOUTH)
                    / constants.GRID_SIZE
                )
            case _:
                return 0.0

    # ---------- OUTPUT BEHAVIOR ----------
    def activate(self, creature) -> None:
        match self:
            case NeuronRole.MOVE_WEST:
                creature.move(Direction.WEST)
            case NeuronRole.MOVE_NORTH:
                creature.move(Direction.NORTH)
            case NeuronRole.MOVE_EAST:
                creature.move(Direction.EAST)
            case NeuronRole.MOVE_SOUTH:
                creature.move(Direction.SOUTH)
            case NeuronRole.MOVE_LEFT:
                creature.move(Turn.LEFT)
            case NeuronRole.MOVE_FORWARD:
                creature.move(Turn.FORWARD)
            case NeuronRole.MOVE_RIGHT:
                creature.move(Turn.RIGHT)
            case NeuronRole.MOVE_BACKWARD:
                creature.move(Turn.BACKWARD)
            case NeuronRole.MOVE_RANDOM:
                creature.move(Turn.RANDOM)
            case NeuronRole.TURN_LEFT:
                creature.choose_move_direction(Turn.LEFT)
            case NeuronRole.TURN_RIGHT:
                creature.choose_move_direction(Turn.RIGHT)
            case _:
                pass
