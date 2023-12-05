from dataclasses import dataclass
from pathlib import Path


@dataclass
class ScratchCard:
    id: int
    winning_nums: set[int]
    scratch_nums: list[int]

    card_multiplier = 1

    def addToMultiplier(self, x: int) -> None:
        self.card_multiplier += x

    # Return the number of winning numbers for the card
    def getWinCount(self) -> int:
        point_count = 0
        for x in self.scratch_nums:
            if x in self.winning_nums:
                point_count += 1
        return point_count

    # Return the win points from doubling for every game after 1.
    def getWinningPoints(self) -> int:
        win_count = self.getWinCount()
        
        point_total = 0
        if win_count > 0:
            win_count -= 1
            point_total += 1

            while win_count != 0:
                point_total *= 2
                win_count -= 1
        return point_total
    
    # Updates input dict of games with their multiples and returns the current game's multiplier
    def processMultiples(self, all_games: dict) -> None:
        mult = self.card_multiplier
        win_count = self.getWinCount()
        # Win 4 add current multiplier to next 4 card's multiplier
        # Win 2 add current multiplier to next 2 card's multiplier
        while win_count != 0:
            next = self.id + win_count
            all_games[next].addToMultiplier(mult)
            win_count -= 1
        
def parseGameId(gamestr: str) -> int:
    return int(gamestr.split()[-1])

def parseScratchCards(file_path: Path) -> list[ScratchCard]:
    with open(file_path, "r") as f:
        rows = []
        for row in f:
            game_split = row.split(':')
            nums = game_split[1].split('|')
            rows.append(ScratchCard(parseGameId(game_split[0]), nums[0].split(), nums[1].split()))
        return rows


def main():
    file_name = "dec04_input.txt"
    # file_name = "testdata1-13.txt"

    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / file_name

    games = parseScratchCards(file_path)

    game_dict = {card.id: card for card in games}
    # print(game_dict)

    sum_points = 0
    for game in games:
        sum_points += game.getWinningPoints()
    print(sum_points)

    # Part 2 expected total is 30 for test data
    sum_cards = 0
    for card in games:
        sum_cards += card.card_multiplier
        card.processMultiples(game_dict)
    print(sum_cards)


    


if __name__ == "__main__":
    main()
