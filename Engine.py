from config import DEFAULT_GAMES_ANALYSES_FILENAME, ENGINE_PATH
from tqdm import tqdm
import chess.engine
import pickle
import os.path
from utils import get_game_id

MAX_ANALYSIS_SECONDS_PER_MOVE = 0.50


class Engine:
    engine_path = None
    engine = None
    games_analyses = {}

    def __init__(self, engine_path=ENGINE_PATH, games_analyses_filename=DEFAULT_GAMES_ANALYSES_FILENAME):
        self.set_engine(engine_path)
        self.load_games_analyses(games_analyses_filename)

    def set_engine(self, engine_path=None):
        if engine_path:
            self.engine_path = engine_path

        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)

    def analyse_game(self, game):
        if not self.engine:
            print('Missing engine to analyse game')
            return

        game_id = get_game_id(game)

        # If there is already an analysis in cache, return it
        if game_id in self.games_analyses:
            return self.games_analyses[game_id]

        board = game.board()
        analysis = {
            'game_scores': [],
            'best_moves': []
        }

        for move in game.mainline_moves():
            info = self.engine.analyse(board, chess.engine.Limit(time=MAX_ANALYSIS_SECONDS_PER_MOVE))

            analysis['game_scores'].append(info["score"])
            if info.pv:
                analysis['best_moves'].append(info.pv[0])

            board.push(move)

        self.games_analyses[game_id] = analysis

        return analysis

    def get_game_analysis(self, game):
        game_id = get_game_id(game)

        if game_id in self.games_analyses:
            return self.games_analyses[game_id]
        else:
            return None

    def analyse_all_games(self, games):
        games_analyses = {}
        for game in tqdm(games):
            game_id = get_game_id(game)
            games_analyses[game_id] = self.analyse_game(game)

        return games_analyses

    def save_games_analyses(self, filename=DEFAULT_GAMES_ANALYSES_FILENAME):
        with open(filename, 'wb') as handle:
            pickle.dump(self.games_analyses, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_games_analyses(self, filename=DEFAULT_GAMES_ANALYSES_FILENAME):
        if not filename or not os.path.isfile(filename):
            print('No previous games analyses file could be found with name : ' + filename)
            return

        with open(filename, 'rb') as handle:
            games_analyses = pickle.load(handle)
            self.games_analyses = {**self.games_analyses, **games_analyses}

        return self.games_analyses
