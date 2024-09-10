from enum import Enum

class GameState(Enum):
    ENTRYPOINT = 0
    WAITING_START_SCREEN = 1
    CHOOSE_PSEUDO = 2
    FIND_SOMEONE = 3
    SELECTING_COUNTRY = 4
    START_GAME = 5
    IN_GAME = 6
    CREDITS = 7
    RULE = 8
