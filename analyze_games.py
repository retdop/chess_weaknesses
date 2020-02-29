import chess.engine
from chess.pgn import read_game
from tqdm import tqdm
import pickle


def load_games(filename):
    with open(filename) as games_file:
        games = []
        game = None
        while (game or games == []) and len(games) < 300:
            game = read_game(games_file)
            if game is not None:
                games.append(game)
    return games


def save_scores(games):
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
    with open('./lichess_pavermesh_2019-11-05.scores.pkl', 'wb') as handle:
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


if __name__ == '__main__':
    games_filename = 'lichess_pavermesh_2019-11-05.pgn'
    pavermesh_games = load_games(games_filename)
    # save_scores(pavermesh_games)
    # scores_filename = './lichess_pavermesh_2019-11-05.scores.pkl'
    # scores = load_scores(scores_filename)
    for game in tqdm(pavermesh_games):
        print(thematize_game(game))
