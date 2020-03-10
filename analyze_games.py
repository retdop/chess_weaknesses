import chess.engine
from chess.pgn import read_game
from tqdm import tqdm
import pickle
import numpy as np
import matplotlib.pyplot as plt


def load_games(filename):
    with open(filename) as games_file:
        games = []
        game = None
        while (game or games == []) and len(games) < 300:
            game = read_game(games_file)
            if game is not None:
                games.append(game)
    return games


def save_scores(games, filename='./lichess_pavermesh_2019-11-05.scores.pkl'):
    engine = chess.engine.SimpleEngine.popen_uci("./stockfish-10-linux/src/stockfish")
    # args="--threads 4")

    # board = games[5].board()
    # print(board)
    # info = engine.analyse(board, chess.engine.Limit(time=0.100))
    # print("Score:", info["score"])
    # print()

    scores = {}
    for game in tqdm(games):
        game_id = game.headers['Site'].split('/')[-1]
        board = game.board()
        game_scores = []
        for move in game.mainline_moves():
            # print(move)
            # print("Score:", info_small["score"])
            # print(board)
            board.push(move)
            info = engine.analyse(board, chess.engine.Limit(time=0.10))
            game_scores.append(info["score"])
        scores[game_id] = game_scores
    with open(filename, 'wb') as handle:
        pickle.dump(scores, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_scores(filename):
    with open(filename, 'rb') as handle:
        scores_loaded = pickle.load(handle)
    return scores_loaded


def thematize_game(game):
    board = game.board()
    themes = {}
    for i, move in enumerate(game.mainline_moves()):
        # print(move)
        # print("Score:", info_small["score"])
        # print(board)
        board.push(move)
        themes[str(i)] = get_themes(board)
    return themes


def get_themes(position):
    themes = set()
    for move in position.legal_moves:
        position.push(move)
        if position.is_check():
            themes.add('check')
        position.pop()

    if any(position.is_pinned(chess.WHITE, square) for square in chess.SQUARES):
        themes.add('absolute pin')
    return themes


def get_position_score(pov_score, color):
    if pov_score.pov(color).is_mate():
        if pov_score.pov(color).mate() > 0:
            return 100
        else:
            return -100
    else:
        return pov_score.pov(color).score()


def plot_themes_differences(games, scores):
    for game in tqdm(games):
        pavermesh_color = 0 if game.headers['White'] == 'pavermesh' else 1
        game_id = game.headers['Site'].split('/')[-1]
        game_themes = thematize_game(game)
        if game_id not in scores:
            continue

        game_scores = scores[game_id]

        game_score_differences = [get_position_score(game_scores[i+1], pavermesh_color) - get_position_score(game_scores[i], pavermesh_color)
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
        plt.savefig('figs/pavermesh_' + game_id + '_themes successes.png')
        plt.close()


if __name__ == '__main__':
    games_filename = 'lichess_pavermesh_2019-11-05.pgn'
    pavermesh_games = load_games(games_filename)
    scores_filename = './lichess_pavermesh_2019-11-05.scores.pkl'
    # save_scores(pavermesh_games, scores_filename)
    pavermesh_scores = load_scores(scores_filename)
    plot_themes_differences(pavermesh_games, pavermesh_scores)
