from enum import Enum

from nba_api.stats.library.parameters import (
    PlayerOrTeamAbbreviation,
    SeasonTypeAllStar,
)


class GameResult(str, Enum):
    WIN = 'W'
    LOSS = 'L'


class OverUnderResult(str, Enum):
    OVER = 'O'
    UNDER = 'U'
    PUSH = 'P'


class SeasonType(str, Enum):
    REGULAR = SeasonTypeAllStar.regular
    PLAYOFFS = SeasonTypeAllStar.playoffs


class SpreadResult(str, Enum):
    WIN = 'W'
    LOSS = 'L'
    PUSH = 'P'


class StatsType(str, Enum):
    PLAYER = PlayerOrTeamAbbreviation.player
    TEAM = PlayerOrTeamAbbreviation.team
