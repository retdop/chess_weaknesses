import os
import pickle
from glob import glob

import chess.engine
from chess.engine import EngineError
from tqdm import tqdm

from config import ENGINE_PATH
from utils import get_game_id

MAX_ANALYSIS_SECONDS_PER_MOVE = 0.50
SCORES_DIRECTORY = 'engine_scores/'


class Engine:
    engine_path = None
    engine = None
    games_analyses = {}

    def __init__(self, engine_path=ENGINE_PATH):
        self.set_engine(engine_path)
        self.load_games_analyses()

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
            try:
                games_analyses[game_id] = self.analyse_game(game)
            except EngineError as e:
                print(game_id)
                print(e)
                continue
            with open(SCORES_DIRECTORY + game_id + '.scores.pkl', 'wb') as handle:
                pickle.dump(games_analyses[game_id], handle, protocol=pickle.HIGHEST_PROTOCOL)
        return games_analyses

    def load_games_analyses(self):
        for filename in glob(os.path.join(SCORES_DIRECTORY, '*.scores.pkl')):
            with open(os.path.join(os.getcwd(), filename), 'rb') as handle:  # open in readonly mode
                game_analysis = pickle.load(handle)
                game_id = filename.split('.')[0].split('/')[-1]
                self.games_analyses = {**self.games_analyses, game_id: game_analysis}
        return self.games_analyses
