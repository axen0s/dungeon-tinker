from abc import ABC, abstractmethod


class BaseDungeonGenerator(ABC):
    """kwargs for dungeon in [(Name of argument, type of argument), ...] format"""
    dungeon_kwargs: list[tuple[str, type]] = []

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        """Dungeon format is currently true for wall being at coord, false for not/being empty"""
        self.dungeon: list[list[bool]] = []

    @abstractmethod
    def generate(self) -> None:
        """
        This method should always modify our dungeon using the algorithm of the subclass's choice.
        :return:
        """
        pass

    def get_dungeon_lines(self) -> list[str]:
        """
        :return: dungeon in printable/displayable line format
        """
        rows = []
        if self.dungeon:
            for row in self.dungeon:
                rows.append("".join(['#' if cell else '.' for cell in row]))
        return rows
