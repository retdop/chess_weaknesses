from abc import ABC, abstractmethod


class Theme(ABC):
    @abstractmethod
    def is_on_position(self, position, player_color):
        pass

    def get_name(self):
        return self.__class__.__name__
