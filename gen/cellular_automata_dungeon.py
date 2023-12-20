import random
from gen.base_dungeon_gen import BaseDungeonGenerator


class CADungeonGen(BaseDungeonGenerator):
    dungeon_kwargs: list[tuple[str, type, any]] = [("Iterations", int, 5), ("Birth Threshold", int, 4),
                                                   ("Death Threshold", int, 3), ("Initial Probability", float, 0.4)]

    def generate(self, seed: int = None, **kwargs) -> None:  # -> list[list[bool]]:
        kwargs = kwargs['kwargs']

        def count_neighbors(_dungeon, x, y) -> int:
            count = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if 0 <= x + k < len(_dungeon) and 0 <= l + j < len(_dungeon[0]) and (k != 0 or l != 0):
                        count += _dungeon[x + k][y + l]
            return count

        if seed:
            random.seed(seed)
        dungeon = [[random.random() < kwargs["Initial Probability"] for _ in range(self.width)] for _ in
                   range(self.height)]
        for _ in range(kwargs["Iterations"]):
            new_dungeon = [[False] * len(dungeon[0]) for _ in range(len(dungeon))]
            for i in range(len(dungeon)):
                for j in range(len(dungeon[0])):
                    neighbors = count_neighbors(dungeon, i, j)
                    if dungeon[i][j]:
                        new_dungeon[i][j] = neighbors > kwargs["Death Threshold"]
                    else:
                        new_dungeon[i][j] = neighbors >= kwargs["Birth Threshold"]
            dungeon = new_dungeon
        self.dungeon = dungeon
