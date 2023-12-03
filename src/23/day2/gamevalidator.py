from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GameSet:
    cubes: dict[str, int]

@dataclass
class Game:
    id: int
    sets: list[GameSet]

# Parses the game string to see if it is valid for the expected input.
# Returns the game's ID or 0 if the game is invalid.
def getValidGameId(game_str: str, expected: dict[str, int]) -> int:
    game = parseGameStr(game_str)

    for game_set in game.sets:
        for k, v in game_set.cubes.items():
            if expected[k] < v:
                return 0

    return game.id

def parseGameStr(game_str: str) -> Game:
    gamecube_split = game_str.split(':')
    game_id_str = gamecube_split[0]
    game_id = int(game_id_str.split(' ')[-1])
    sets_strs = gamecube_split[1].split(';')

    return Game(game_id, [parseGameSetStr(gset) for gset in sets_strs])


def parseGameSetStr(game_set_str: str) -> GameSet:
    cube_strs = game_set_str.split(',')
    cubes = {}
    for colorstr in cube_strs:
        cubes.update(parseColor(colorstr))

    return GameSet(cubes)

def parseColor(s: str) -> dict[str, int]:
    spl = s.split()
    return {spl[1]: int(spl[0])}

def sumValidGames(file_path: str) -> None:
     # 12 red cubes, 13 green cubes, and 14 blue cubes
    expected = {'red': 12, 'green': 13, 'blue': 14}
    with open(file_path, "r") as f:
        sum = 0
        line_number = 1
        for line in f:
            sum += getValidGameId(line, expected)
            line_number += 1
        
        print("ID Sum: " + str(sum))

def getMinimumBag(game: Game) -> GameSet:
    min_cubes = defaultdict(lambda: 0)

    for g in game.sets:
        for k,v in g.cubes.items():
            if v > min_cubes[k]:
                min_cubes[k] = v
    return GameSet(min_cubes)

def getGameSetPower(game_set: GameSet) -> int:
    power = 1
    for v in game_set.cubes.values():
        power *= v
    return power

def sumGamePowers(file_path: str) -> None:
    with open(file_path, 'r') as f:
        sum = 0
        line_number = 1
        for line in f:
            min_bag = getMinimumBag(parseGameStr(line))
            sum += getGameSetPower(min_bag)
        
        print('sum of powers is: ' + str(sum))


def main():
    file_name = "dec02_input.txt"
    # file_name = "testdata1.txt"

    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / file_name

    # sumValidGames(file_path)
    sumGamePowers(file_path)

    # print(str(myValidator.solveGame('Game 1: 1 blue, 3 red, 6 pink; 3 blue; 2 red', {'blue': 5, 'pink': 10, 'red': 5})))
    # print(str(myValidator.solveGame('Game 1: 1 blue, 3 red, 6 pink; 3 blue; 2 red', {'blue': 1, 'pink': 10, 'red': 5})))
    # print(str(myValidator.parseGameStr('Game 1: 1 blue, 3 red, 6 pink; 3 blue; 2 red')))
    

if __name__ == "__main__":
    main()

