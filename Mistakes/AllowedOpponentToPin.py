from Mistakes.Mistake import Mistake
import chess


class AllowedOpponentToPin(Mistake):
    # Could be improved as it only checks if the opponent pins on his next turn and not a bit later
    def has_happened_on_position(self, prev_pos, move, best_move, opponent_best_move,  score_diff):

        color_to_play = prev_pos.turn
        prev_pinned_squares = []

        # Find all pieces of the player that are already pinned
        for square in chess.SQUARES:
            if prev_pos.is_pinned(color_to_play, square):
                prev_pinned_squares.append(square)

        # Make the moves
        prev_pos.push(move)
        prev_pos.push(opponent_best_move)

        newly_pinned_squares = []

        # Find all newly pinned squares that weren't pinned before
        for square in chess.SQUARES:
            if prev_pos.is_pinned(color_to_play, square):
                if square not in prev_pinned_squares:
                    newly_pinned_squares.append(square)

        # Undo the moves
        prev_pos.pop()
        prev_pos.pop()

        # If there are new pinned pieces then the last move is assumed to have created a pin.
        # Please be aware that the newly pinned piece is not necessarily the piece that moved.
        # The move could have created a discovery like a pawn moving for example.
        if len(newly_pinned_squares) > 0:
            return True
        else:
            return False
