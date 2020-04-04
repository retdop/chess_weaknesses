from abc import abstractmethod
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from utils import get_player_color, get_position_score


class ThemeAnalyzer:
    player = ''

    @property
    @abstractmethod
    def games(self):
        pass

    @property
    @abstractmethod
    def engine(self):
        pass

    def thematize_game(self, raw_game):
        board = raw_game.board()
        themes = {}
        for i, move in enumerate(raw_game.mainline_moves()):
            # print(move)
            # print("Score:", info_small["score"])
            # print(board)
            board.push(move)
            themes[str(i)] = self.get_themes(raw_game, board)
        return themes

    def get_themes(self, raw_game, position):
        player_color = get_player_color(self.player, raw_game)
        themes = set()
        for theme in themes:
            if theme.is_on_position(position, player_color):
                themes.add(theme.get_name())
        return themes

    def thematize_games(self):
        print('Finding themes')
        for game_id, game in tqdm(self.games.items()):
            game['themes'] = self.thematize_game(game['raw'])

    def plot_themes_differences(self):
        print('Plotting themes scores differences')
        for game_id, game in tqdm(self.games.items()):
            player_color = get_player_color(self.player, game['raw'])
            game_themes = game['themes']
            game_engine_analysis = game['engine_analysis']
            if game_engine_analysis is None:
                continue
            game_scores = game_engine_analysis['game_scores']
            game_score_differences = [get_position_score(game_scores[i + 1], player_color)
                                      - get_position_score(game_scores[i], player_color)
                                      for i in range(len(game_scores) - 1)]
            all_game_themes = set(theme for position_themes in game_themes.values() for theme in position_themes)
            themes_score_differences = {
                theme: [game_score_differences[i] for i in range(len(game_score_differences))
                        if theme in game_themes[str(i)]]
                for theme in all_game_themes
            }
            plt.hist(game_score_differences, bins=20, alpha=0.7, label='All scores differences')
            for theme, theme_score_differences in themes_score_differences.items():
                plt.hist(theme_score_differences, bins=20, alpha=0.7, label=theme + ' scores differences')
            plt.legend()
            # plt.show()
            os.makedirs('./figures/', exist_ok=True)
            plt.savefig('figures/' + self.player + '_' + game_id + '_themes successes.png')
            plt.close()
