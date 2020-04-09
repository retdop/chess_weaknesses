from config import GAMES_FILENAME
from chess.pgn import read_game
from Engine import Engine
from utils import get_game_id
from MistakeAnalyzer import MistakeAnalyzer
from ThemeAnalyzer import ThemeAnalyzer
from EndgameAnalyzer import EndgameAnalyzer

MAX_NUMBER_OF_GAMES_TO_ANALYSE = 50
GAMES_ANALYSES_FILENAME = 'scores.pkl'
PLAYER_NAME = 'pavermesh'


class Analysis(MistakeAnalyzer, ThemeAnalyzer, EndgameAnalyzer):
    engine = None
    games_filename = None
    games = {}
    player = None

    # dict games structure is
    # { game_id: { raw: chess_game, found_mistakes: list, }

    # dict game_engine_analysis structure is
    # { game_scores: List, best_moves: List}

    def __init__(self, engine=None, games_filename=None,
                 calculate_scores=False,
                 max_number_of_games_to_analyse=MAX_NUMBER_OF_GAMES_TO_ANALYSE,
                 player=PLAYER_NAME):
        self.player = player
        self.max_number_of_games_to_analyse = max_number_of_games_to_analyse
        self.engine = engine or Engine()
        self.load_games(games_filename=games_filename)
        self.engine.load_games_analyses()
        if calculate_scores:
            self.pre_compute_engine_analyses()
        for game in self.games.values():
            game['engine_analysis'] = self.engine.get_game_analysis(game)

    def set_games_filename(self, filename):
        self.games_filename = filename

    def pre_compute_engine_analyses(self):
        games = [self.games[game_id]['raw'] for game_id in self.games]
        self.engine.analyse_all_games(games)

    def load_games(self, games_filename=None):
        if not games_filename and not self.games_filename:
            print('Missing a filename for the pgn to load')
            return

        if games_filename:
            self.set_games_filename(games_filename)

        pgn = self.games_filename

        with open(pgn) as filename:
            games = {}
            game = None

            while (game or len(games) == 0) and len(games) < self.max_number_of_games_to_analyse:
                game = read_game(filename)
                if game is not None:
                    game_id = get_game_id(game)
                    games[game_id] = {}
                    games[game_id]['raw'] = game

        self.games = games

        return self.games


if __name__ == '__main__':
    analysis = Analysis(games_filename=GAMES_FILENAME,
                        calculate_scores=True,
                        player=PLAYER_NAME)
    analysis.find_mistakes()
    analysis.thematize_games()
    analysis.plot_themes_differences()
    analysis.endgamize_games()
    analysis.plot_endgames_differences()
