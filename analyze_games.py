import chess.engine
from chess.pgn import read_game
from tqdm import tqdm

games_file_name = 'lichess_pavermesh_2019-11-05.pgn'

games_file = open(games_file_name)

games = []
game = None
while (game or games == []) and len(games) < 3:
    game = read_game(games_file)
    if game is not None:
        games.append(game)

engine = chess.engine.SimpleEngine.popen_uci("/home/gabriel/fun/chess/stockfish-10-linux/src/stockfish")
# args="--threads 4")

# board = games[5].board()
# print(board)
# info = engine.analyse(board, chess.engine.Limit(time=0.100))
# print("Score:", info["score"])
# print()

scores = []
for game in tqdm(games):
    board = game.board()
    game_scores = []
    for move in game.mainline_moves():
        # print(move)
        # print("Score:", info_small["score"])
        # print(board)
        board.push(move)
        info = engine.analyse(board, chess.engine.Limit(time=0.10))
        game_scores.append(info["score"])
    scores.append(game_scores)

print()
