from abc import ABC, abstractmethod


class Mistake(ABC):
    @abstractmethod
    def has_happened_on_position(self, prev_pos, move, best_move, opponent_best_move, score_diff):
        pass

    def get_name(self):
        return self.__class__.__name__
