from Themes.Theme import Theme


class Check(Theme):
    def is_on_position(self, position, _):

        for move in position.legal_moves:
            position.push(move)
            if position.is_check():
                return True
            position.pop()
        return False
