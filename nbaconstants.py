from nba_api.stats.library.parameters import (
    Season,
    PlayerOrTeamAbbreviation,
    SeasonTypeAllStar,
)
CURRENT_SEASON = '2022-23'
MIN_SEASON = 2006  # earliest available season in Covers data
REGULAR_SEASON = SeasonTypeAllStar.regular
PLAYER = PlayerOrTeamAbbreviation.player
TEAM = PlayerOrTeamAbbreviation.team
