from enum import Enum


class MatchStatus(Enum):
    NOT_STARTED = 1
    FINISHED = 2
    LOCAL_PLAYER_TURN = 3
    REMOTE_PLAYER_TURN = 4
    ABANDONED = 5
