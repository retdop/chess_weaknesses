from chess import WHITE, BLACK


def get_game_id(game):
    if 'raw' in game:
        return get_game_id(game['raw'])
    else:
        return game.headers['Site'].split('/')[-1]


def get_position_score(pov_score, color):
    if pov_score.pov(color).is_mate():
        if pov_score.pov(color).mate() > 0:
            return 100
        else:
            return -100
    else:
        return pov_score.pov(color).score()


def get_player_color(player, raw_game):
    return WHITE if raw_game.headers['White'] == player else BLACK
