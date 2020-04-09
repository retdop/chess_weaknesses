from abc import abstractmethod
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from utils import get_player_color, get_position_score
from Themes import themes


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
        game_themes = {}
        for i, move in enumerate(raw_game.mainline_moves()):
            board.push(move)
            game_themes[str(i)] = self.get_themes(raw_game, board)
        return game_themes

    def get_themes(self, raw_game, position):
        player_color = get_player_color(self.player, raw_game)
        position_themes = set()
        for theme in themes:
            if theme.is_on_position(position, player_color):
                position_themes.add(theme.get_name())
        return position_themes

    def thematize_games(self):
        print('Finding themes')
        for game_id, game in tqdm(self.games.items()):
            game['themes'] = self.thematize_game(game['raw'])

    def plot_themes_differences(self):
        print('Plotting themes scores differences')
        os.makedirs('./figures/' + self.player, exist_ok=True)
        games_score_differences = []
        games_score_diff = {}
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
            games_score_differences.extend(game_score_differences)
            whole_game_themes = set(theme for position_themes in game_themes.values() for theme in position_themes)
            game_score_diff = {
                theme: [game_score_differences[i] for i in range(len(game_score_differences))
                        if theme in game_themes[str(i)]]
                for theme in whole_game_themes
            }
            for theme in whole_game_themes:
                games_score_diff[theme] = games_score_diff[theme] + game_score_diff[theme] \
                    if theme in games_score_diff else game_score_diff[theme]

            plt.hist(game_score_differences, bins=50, range=(-2000, 2000), alpha=0.7, label='All scores differences')
            for theme, theme_score_differences in game_score_diff.items():
                plt.hist(theme_score_differences, bins=50, range=(-2000, 2000), alpha=0.7,
                         label=theme + ' scores differences')
            plt.legend()
            plt.title(game_id + ' themes analysis')
            plt.savefig('figures/' + self.player + '/' + game_id + '_themes successes.png')
            plt.close()

        plt.hist(games_score_differences, bins=50, range=(-2000, 2000), alpha=0.7, label='All scores differences')
        for theme, theme_score_differences in games_score_diff.items():
            plt.hist(theme_score_differences, bins=50, range=(-2000, 2000), alpha=0.7,
                     label=theme + ' scores differences')
        plt.legend()
        plt.title('All games themes analysis')
        plt.savefig('figures/' + self.player + '/' + 'themes successes.png')
        plt.close()

        plt.hist(games_score_differences, bins=100, range=(-500, 500), alpha=0.7, label='All scores differences')
        for theme, theme_score_differences in games_score_diff.items():
            plt.hist(theme_score_differences, bins=100, range=(-500, 500), alpha=0.7,
                     label=theme + ' scores differences')
        plt.legend()
        plt.ylim((0, 20))
        plt.title('All games themes analysis - zoomed')
        plt.savefig('figures/' + self.player + '/' + 'themes successes_zoomed.png')
        plt.close()
