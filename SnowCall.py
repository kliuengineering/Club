from typing import List, Dict
import re
from functools import singledispatch


# << interface >>
class SolutionBuilder:
    # input validation
    def validate(self, s: str) -> str:
        if len(s) < 10:
            print("Phone # length is incorrect.\n")
            raise ValueError

        # only takes the first 10 characters
        s = s[:12].replace("-", "").lower()    
        
        # pattern recognition
        pattern = r"^[a-z\d]+$"
        if not re.match(pattern, s):
            print("Phone # pattern is incorrect.\n")
            raise ValueError
        
        # print(s, " -> passed test")
        return s


# concrete implementation - solution A
class SolutionA(SolutionBuilder):
    def __init__(self):
        super().__init__()
        self.contact_list = []
        self.hashmap = {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "a": "2",
            "b": "2",
            "c": "2",
            "d": "3",
            "e": "3",
            "f": "3",
            "g": "4",
            "h": "4",
            "i": "4",
            "j": "5",
            "k": "5",
            "l": "5",
            "m": "6",
            "n": "6",
            "o": "6",
            "p": "7",
            "q": "7",
            "r": "7",
            "s": "7",
            "t": "8",
            "u": "8",
            "v": "8",
            "w": "9",
            "x": "9",
            "y": "9",
            "z": "9"
        }
    
    def __convert(self, s) -> str:
        s_converted = "".join( map( lambda itr: self.hashmap[itr], s ) )
        return s_converted
    
    def __add_dash(self, s) -> str:
        return s[0:3] + "-" + s[3:6] + "-" + s[6:10]

    def __algorithm(self, s) -> None:
        s_validated = super().validate(s)
        s_converted = self.__convert(s_validated)
        s_dashed = self.__add_dash(s_converted)
        self.contact_list.append(s_dashed)

    def print(self) -> None:
        for itr in self.contact_list:
            print(itr)

    # polymorphism based on type checking
    def convert_contact(self, import_data) -> None:
        if isinstance(import_data, str):
            # print(f"Processing single contact: {import_data}")  # Debug print
            self.__algorithm(import_data)

        elif isinstance(import_data, list):
            # print(f"Processing list of contacts: {import_data}")  # Debug print
            for itr in import_data:
                self.__algorithm(itr)
                
        else:
            raise NotImplementedError("Unsupported type found")


# main routine
def main():
    solutionA = SolutionA()

    numberA = "88-SNOW-5555"
    numberB = "519-888-4567"
    numberC = "BUY-MORE-POP"
    numberD = "416-PIZZA-BOX"
    numberE = "5059381123"
    
    contact = [numberA, numberB, numberC, numberD, numberE]
    # print(f"Type of contact: {type(contact)}")  # Debug print to see the type

    solutionA.convert_contact(contact)
        
    solutionA.print()


if __name__ == "__main__":
    main()