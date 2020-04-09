from chess import WHITE, BLACK


def get_game_id(game):
    if 'raw' in game:
        return get_game_id(game['raw'])
    else:
        return game.headers['Site'].split('/')[-1]


def get_position_score(pov_score, color):
    if pov_score.pov(color).is_mate():
        if pov_score.pov(color).mate() > 0:
            return 1000
        else:
            return -1000
    else:
        return max(min(pov_score.pov(color).score(), 1000), -1000)


def get_player_color(player, raw_game):
    return WHITE if raw_game.headers['White'] == player else BLACK
