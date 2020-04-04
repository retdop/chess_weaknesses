from Themes.Theme import Theme
from chess import SQUARES


class AbsolutePin(Theme):
    def is_on_position(self, position, player_color):
        return any(position.is_pinned(player_color, square) for square in SQUARES)
