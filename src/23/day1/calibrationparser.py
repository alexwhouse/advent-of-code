from pathlib import Path
import regex

class CalibrationParser:

    word_numbers = {"one": 1,
                    "two": 2,
                    "three": 3,
                    "four": 4,
                    "five": 5,
                    "six": 6,
                    "seven": 7,
                    "eight": 8,
                    "nine": 9}
    

    p = regex.compile(r"\L<name>", name=word_numbers.keys())

    def sumCalibrations(self, fileName: str) -> int:
        with open(fileName, "r") as f:
            sum = 0
            for line in f:
                sum += self.parseCalibrationLine(line)
            
            return sum
    
    def parseCalibrationLine(self, line: str) -> int:
        # returns the number parsed from the calibration string of the first and last digit.
        first = ""
        last = ""

        substr = ""
        for c in line:
            if not c.isnumeric():
                substr += c
                continue
            if not first:
                # TODO check substr if it is numeric first
                numbers = self.getNumericValue(substr)
                if numbers:
                    first = numbers[0]
                else:
                    first = c
                substr = ""
            else:
                last = c
                substr = ""
        
        numbers = self.getNumericValue(substr)
        if numbers:
            if not first:
                first = numbers[0]
            last = numbers[-1]

        if not last:
            last = first

        if not first:
            print("No value found for " + line)
            return 0
        return int(first + last)
    
    def getNumericValue(self, s: str) -> list[int]:
        # Returns all numeric values contained in string s in the order they appeared
        return [str(self.word_numbers[x]) for x in self.p.findall(s)]


    
def main():
    myParser = CalibrationParser()
    file_name = "dec01_input.txt"
    # file_name = "testdata2.txt"
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / file_name

    print(myParser.sumCalibrations(file_path))
    # print(myParser.parseCalibrationLine("eightwothree"))

    # print(myParser.getNumericValue("eighttwothree"))

if __name__ == "__main__":
    main()

