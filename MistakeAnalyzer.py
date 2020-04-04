from Mistakes import mistakes
from utils import get_game_id, get_player_color, get_position_score
from tqdm import tqdm
from abc import abstractmethod


class MistakeAnalyzer:
    player = NotImplementedError

    @property
    @abstractmethod
    def games(self):
        pass

    @property
    @abstractmethod
    def engine(self):
        pass

    def look_for_mistakes_in_game(self, raw_game, game_engine_analysis):
        game_id = get_game_id(raw_game)

        if not game_engine_analysis:
            print('Analysis could not retrieve analysis for game : ' + game_id)
            return

        score = game_engine_analysis['game_scores'][0]
        game_mistakes = []

        board = raw_game.board()
        for i, move in enumerate(raw_game.mainline_moves()):
            if i == len(game_engine_analysis['game_scores']) - 2:
                break
            player_color = get_player_color(self.player, raw_game)

            new_score = game_engine_analysis['game_scores'][i]
            prev_score_value = get_position_score(score, player_color)
            score_diff = abs(prev_score_value - get_position_score(new_score, player_color))
            score = new_score

            mistakes_for_this_move = []

            # Score is an integer so adding a float prevents it to be 0
            if score_diff > 30 and (prev_score_value == 0 or abs(score_diff / prev_score_value) > 0.1):
                best_move = game_engine_analysis['best_moves'][i]
                opponent_best_move = game_engine_analysis['best_moves'][i + 1]

                if move != best_move:
                    for mistake in mistakes:
                        has_happened = mistake.has_happened_on_position(board, move,
                                                                        best_move,
                                                                        opponent_best_move,
                                                                        score_diff)
                        if has_happened:
                            mistakes_for_this_move.append(mistake.get_name())

            board.push(move)
            game_mistakes.append(mistakes_for_this_move)

        return game_mistakes

    def find_mistakes(self):
        print('Finding mistakes')
        for game_id, game in tqdm(self.games.items()):
            game['mistakes'] = self.look_for_mistakes_in_game(game['raw'], game['engine_analysis'])
        return
