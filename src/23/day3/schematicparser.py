from collections import deque
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd


@dataclass
class AdjacentValue:
    val: str
    i: int
    j: int

    def curr_val(self, schematic: pd.array) -> str:
        return schematic[self.i][self.j]


def parseSchematicFile(file_path: Path) -> np.array:
    with open(file_path, "r") as f:
        rows = []
        for line in f:
            rows.append(list(line.strip()))
        return np.array(rows)


def isValidPos(i: int, j: int, n: int, m: int) -> bool:
    if i < 0 or j < 0 or i > n - 1 or j > m - 1:
        return False
    return True


# Function that returns all adjacent elements
# sourced from https://www.geeksforgeeks.org/find-all-adjacent-elements-of-given-element-in-a-2d-array-or-matrix/
def getAdjacent(schematic: np.array, i: int, j: int) -> list[AdjacentValue]:
    n = len(schematic)
    m = len(schematic[0])

    adjacents = []

    # Checking for all the possible adjacent positions
    if isValidPos(i - 1, j - 1, n, m):
        adjacents.append(AdjacentValue(schematic[i - 1][j - 1], i - 1, j - 1))
    if isValidPos(i - 1, j, n, m):
        adjacents.append(AdjacentValue(schematic[i - 1][j], i - 1, j))
    if isValidPos(i - 1, j + 1, n, m):
        adjacents.append(AdjacentValue(schematic[i - 1][j + 1], i - 1, j + 1))
    if isValidPos(i, j - 1, n, m):
        adjacents.append(AdjacentValue(schematic[i][j - 1], i, j - 1))
    if isValidPos(i, j + 1, n, m):
        adjacents.append(AdjacentValue(schematic[i][j + 1], i, j + 1))
    if isValidPos(i + 1, j - 1, n, m):
        adjacents.append(AdjacentValue(schematic[i + 1][j - 1], i + 1, j - 1))
    if isValidPos(i + 1, j, n, m):
        adjacents.append(AdjacentValue(schematic[i + 1][j], i + 1, j))
    if isValidPos(i + 1, j + 1, n, m):
        adjacents.append(AdjacentValue(schematic[i + 1][j + 1], i + 1, j + 1))
    return adjacents


def isPartNumberForAnyAdjacentSymbol(adjacents: list[AdjacentValue]) -> bool:
    for s in adjacents:
        if s.val != "." and not s.val.isnumeric():
            return True
    return False


# Gets the full part number from the schematic and replaces it with '.' symbols.
def getFullPartNumber(schematic: np.array, i: int, j: int) -> int:
    row = schematic[i]
    part_num = deque([row[j]])
    row[j] = "."

    jj = j - 1
    while jj >= 0 and np.char.isnumeric(row[jj]):
        part_num.appendleft(row[jj])
        row[jj] = "."
        jj -= 1

    jj = j + 1
    while jj < len(row) and np.char.isnumeric(row[jj]):
        part_num.append(row[jj])
        row[jj] = "."
        jj += 1
    return int("".join(part_num))


def sumValidParts(schematic: np.array) -> int:
    sum = 0
    it = np.nditer(schematic, flags=["multi_index"])
    for x in it:
        if not np.char.isnumeric(x):
            continue
        # print("%s <%s>" % (x, it.multi_index), end=' ')
        adjacents = getAdjacent(schematic, *it.multi_index)
        if isPartNumberForAnyAdjacentSymbol(adjacents):
            # Get full number
            full_num = getFullPartNumber(schematic, *it.multi_index)
            # clear
            sum += full_num

    return sum


def sumGearRatios(schematic: np.array) -> int:
    sum = 0
    it = np.nditer(schematic, flags=["multi_index"])
    for x in it:
        if x != "*":
            continue
        adjacents = getAdjacent(schematic, *it.multi_index)
        adjacent_nums = []
        for adj in adjacents:
            if adj.curr_val(schematic).isnumeric():
                adjacent_nums.append(getFullPartNumber(schematic, adj.i, adj.j))

        if len(adjacent_nums) == 2:
            sum += adjacent_nums[0] * adjacent_nums[1]

    return sum


def main():
    file_name = "dec03_input.txt"
    # file_name = "testdata1-4361.txt"

    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / file_name

    schematic = parseSchematicFile(file_path)
    print(sumValidParts(schematic))

    schematic = parseSchematicFile(file_path)
    print(sumGearRatios(schematic))


if __name__ == "__main__":
    main()
