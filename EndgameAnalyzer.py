import os
from abc import abstractmethod
from collections import Counter

import matplotlib.pyplot as plt
from chess import KING, QUEEN, BISHOP, KNIGHT, ROOK, PAWN
from tqdm import tqdm

from utils import get_player_color, get_position_score

pieces = [QUEEN, BISHOP, KNIGHT, ROOK, PAWN]
piece_material = {
    KING: 50,
    QUEEN: 9,
    ROOK: 5,
    KNIGHT: 3,
    BISHOP: 3,
    PAWN: 1
}
piece_name = {
    KING: 'K',
    QUEEN: 'Q',
    ROOK: 'R',
    KNIGHT: 'N',
    BISHOP: 'B',
    PAWN: 'P'
}


def material(position, player_color):
    return sum([piece_count(position, piece, player_color) * piece_material[piece] for piece in pieces])


def piece_count(position, piece, player_color):
    return len(position.pieces(piece, player_color))


def pieces_count(position, player_color):
    return 'K+' + '+'.join([str(piece_count(position, piece, player_color)) + str(piece_name[piece])
                            for piece in pieces if piece_count(position, piece, player_color) > 0])


class EndgameAnalyzer:
    player = ''

    @property
    @abstractmethod
    def games(self):
        pass

    @property
    @abstractmethod
    def engine(self):
        pass

    def endgamize_game(self, raw_game):
        board = raw_game.board()
        endgames = {}
        has_entered_endgame = False
        for i, move in enumerate(raw_game.mainline_moves()):
            board.push(move)
            endgames[str(i)] = self.get_endgame(raw_game, board, has_entered_endgame)
            has_entered_endgame = endgames[str(i)] is not None
        return endgames

    def get_endgame(self, raw_game, position, has_entered_endgame):
        player_color = get_player_color(self.player, raw_game)
        is_endgame = material(position, player_color) <= 13
        if has_entered_endgame or is_endgame:
            return pieces_count(position, player_color) + ' vs ' + pieces_count(position, 1 - player_color)
        else:
            return None

    def endgamize_games(self):
        print('Finding endgames')
        for game_id, game in tqdm(self.games.items()):
            game['endgames'] = self.endgamize_game(game['raw'])

    def plot_endgames_differences(self):
        print('Plotting endgames scores differences')
        os.makedirs('./figures/' + self.player, exist_ok=True)
        games_score_differences = []
        games_score_diff = {}
        endgames = []
        for game_id, game in tqdm(self.games.items()):
            player_color = get_player_color(self.player, game['raw'])
            game_endgames = game['endgames']
            game_engine_analysis = game['engine_analysis']
            if game_engine_analysis is None:
                continue
            game_scores = game_engine_analysis['game_scores']
            game_score_differences = [get_position_score(game_scores[i + 1], player_color)
                                      - get_position_score(game_scores[i], player_color)
                                      for i in range(len(game_scores) - 1)]
            games_score_differences.extend(game_score_differences)
            whole_game_endgames = set(endgame for endgame in game_endgames.values() if endgame is not None)
            endgames.extend(list(whole_game_endgames))
            if len(whole_game_endgames) < 1:
                continue
            game_score_diff = {
                endgame: [game_score_differences[i] for i in range(len(game_score_differences))
                          if endgame == game_endgames[str(i)]]
                for endgame in whole_game_endgames
            }
            for theme in whole_game_endgames:
                games_score_diff[theme] = games_score_diff[theme] + game_score_diff[theme] \
                    if theme in games_score_diff else game_score_diff[theme]

            plt.hist(game_score_differences, bins=50, range=(-20, 20), alpha=0.7, label='All scores differences')
            for endgame, endgame_score_differences in game_score_diff.items():
                plt.hist(endgame_score_differences, bins=50, range=(-20, 20), alpha=0.7,
                         label=endgame + ' scores differences')
            plt.legend()
            plt.title(game_id + ' endgame analysis')
            # plt.show()
            plt.savefig('figures/' + self.player + '/' + game_id + '_endgames successes.png')
            plt.close()

        most_common_endgames = Counter(endgames).most_common(10)
        plt.hist(games_score_differences, bins=50, range=(-2000, 2000), alpha=0.7, label='All scores differences')
        for theme, theme_score_differences in games_score_diff.items():
            plt.hist(theme_score_differences, bins=50, range=(-2000, 2000), alpha=0.7,
                     label=theme + ' scores differences')
        plt.legend()
        plt.title('All games endgames analysis')
        plt.savefig('figures/' + self.player + '/' + 'endgames successes.png')
        plt.close()

        plt.hist(games_score_differences, bins=100, range=(-500, 500), alpha=0.7, label='All scores differences')
        for endgame, endgame_score_differences in games_score_diff.items():
            if endgame in most_common_endgames:
                plt.hist(endgame_score_differences, bins=100, range=(-500, 500), alpha=0.7,
                         label=endgame + ' scores differences')
        plt.legend()
        plt.ylim((0, 20))
        plt.title('All games endgames analysis - zoomed')
        plt.savefig('figures/' + self.player + '/' + 'endgames successes_zoomed.png')
        plt.close()
