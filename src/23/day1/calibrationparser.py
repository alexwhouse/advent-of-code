from pathlib import Path
import regex

class CalibrationParser:

    word_numbers = {"one": "1",
                    "two": "2",
                    "three": "3",
                    "four": "4",
                    "five": "5",
                    "six": "6",
                    "seven": "7",
                    "eight": "8",
                    "nine": "9"}
    

    p = regex.compile(r"\L<name>", name=word_numbers.keys())

    def sumCalibrations(self, fileName: str) -> int:
        with open(fileName, "r") as f:
            sum = 0
            line_number = 1
            for line in f:
                sum += self.parseCalibrationLine(line, line_number)
                line_number += 1
            
            return sum
    
    def parseCalibrationLine(self, line: str, line_number: int=None) -> int:
        # returns the number parsed from the calibration string of the first and last digit.
        first = ""
        last = ""
        allnums = []

        substr = ""
        for c in line:
            if not c.isnumeric():
                # print("not numeric " + c)
                substr += c
            elif not first:
                # print("not first " + c)
                numbers = self.getNumericValue(substr)
                if numbers:
                    first = numbers[0]
                    allnums.extend(numbers)
                    allnums.append(c)
                    last = c
                else:
                    first = c
                    last = c
                    allnums.append(c)
                substr = ""
            else:
                # print("not last " + c)
                last = c
                # allnums does not include middle word numbers
                allnums.append(c)
                substr = ""
        
        numbers = self.getNumericValue(substr)
        allnums.extend(numbers)
        if numbers:
            if not first:
                first = numbers[0]
            last = numbers[-1]

        if not first:
            print("No value found for " + line)
            return 0
        if first != allnums[0] or last != allnums[-1]:
            print("Mismatch at line: " + str(line_number) + ". line is: " + line)
        return int(first + last)
    
    def getNumericValue(self, s: str) -> list[int]:
        # Returns all numeric values contained in string s in the order they appeared
        # if s.contains(x) for x in self.word_numbers:
        
        return [self.word_numbers[x] for x in self.p.findall(s, overlapped=True)]


def main():
    myParser = CalibrationParser()
    file_name = "dec01_input.txt"
    # file_name = "testdata2.txt"
    # file_name = "testdata_head5-375.txt"
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / file_name

    print(myParser.sumCalibrations(file_path))
    # print(myParser.parseCalibrationLine("sgeightwo3"))
    # print(myParser.parseCalibrationLine("nineight"))

    # print(myParser.getNumericValue("eighttwothree"))

if __name__ == "__main__":
    main()

