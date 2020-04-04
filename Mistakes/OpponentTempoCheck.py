from Mistakes.Mistake import Mistake


class OpponentTempoCheck(Mistake):
    # Still unperfect as the best move could still lead the opponent to check us, while it being intended.
    # Maybe refactor so that Mistake can analyse alternative lines and compare resulting pos ?
    # The issue with analysing new pos is that it takes a long time which can not scale with this analysis.
    def has_happened_on_position(self, prev_pos, move, best_move, opponent_best_move,  score_diff):

        prev_pos.push(move)
        prev_pos.push(opponent_best_move)

        if prev_pos.is_check():
            prev_pos.pop()
            prev_pos.pop()
            return True

        prev_pos.pop()
        prev_pos.pop()
        return False
