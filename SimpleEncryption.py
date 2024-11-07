from typing import List, Union
from abc import ABC, abstractmethod
import re


# << interface >>
class Strategy:
    def __init__(self, keyword: str, string: str) -> None:
        self._keyword = keyword.upper()[:6]
        stripped_string = re.sub(r"[^a-zA-Z]", "", string)
        self._string = stripped_string.upper()[:60]
        self._keyword_matrix = None
        self._string_matrix = None

    # helper ceil()
    def _ceil(self, x: Union[int, float]) -> int:
        if x == int(x):
            return int(x)
        else:
            return int(x) + 1 if x > 0 else int(x)
        
    # helper converter
    def _convert_to_matrix(self, input_string: str, row: int, col: int) -> List:
        char_array = list(input_string)
        return [ char_array[ i * col: (i + 1) * col ] for i in range(row) ]
    
    # helper concatinator
    def _strconcat(self, input_string: str) -> str:
        return "".join(input_string)
    
    # converts matrices back to strings
    def _convert_to_string(self) -> None:
        # concat keyword matrix
        self._keyword = ""
        for itr in self._keyword_matrix:
            self._keyword += self._strconcat(itr)

        # concat string matrix
        self._string = ""
        for itr in self._string_matrix:
            self._string += self._strconcat(itr)

    # converts to ASCII
    def _convert_ASCII_matrix(self) -> None:
        for i in range(len(self._keyword_matrix)):
            for j in range(len(self._keyword_matrix[i])):
                self._keyword_matrix[i][j] = ord(self._keyword_matrix[i][j]) - 65   # offset here

        for i in range(len(self._string_matrix)):
            for j in range(len(self._string_matrix[i])):
                self._string_matrix[i][j] = ord(self._string_matrix[i][j])

    # converts back to STR
    def _ASCII_to_char_matrix(self) -> None:
        for i in range(len(self._keyword_matrix)):
            for j in range(len(self._keyword_matrix[i])):
                self._keyword_matrix[i][j] = chr(self._keyword_matrix[i][j])

        for i in range(len(self._string_matrix)):
            for j in range(len(self._string_matrix[i])):
                self._string_matrix[i][j] = chr(self._string_matrix[i][j])

    # matrix setup
    def _setup(self) -> None:
        col = len(self._keyword)
        row = self._ceil(len(self._string) / col)
        self._keyword_matrix = self._convert_to_matrix(self._keyword, 1, col)
        self._string_matrix = self._convert_to_matrix(self._string, row, col)
        self._convert_ASCII_matrix()

    # run the routine
    @abstractmethod
    def run(self):
        pass

    # main algorithm
    @abstractmethod
    def _algorithm(self):
        pass

    # converts to the shifted matrix
    @abstractmethod
    def _shift_forward(self):
        pass

    @abstractmethod
    def _shift_back(self):
        pass


# encoder
class Encode(Strategy):
    def __init__(self, keyword, string) -> None:
        super().__init__(keyword, string)
        self._encoded_matrix = None

    def _algorithm(self) -> None:
        row = len(self._string_matrix)

        # initialization
        self._encoded_matrix =[ [ 0 for _ in range( len(self._string_matrix[i]) ) ] for i in range(row) ]
        
        for i in range(row):
            for j in range( len(self._string_matrix[i]) ):
                # Calculate the sum of the current character and the keyword offset
                cache = self._string_matrix[i][j] + self._keyword_matrix[0][j % len(self._keyword_matrix[0])]
                if cache >= 90:
                    cache -= 26
                self._encoded_matrix[i][j] = cache
                # print( f"{ self._encoded_matrix[i][j] }, { self._string_matrix[i][j] }, {self._keyword_matrix[0][j]}" )
        self._string_matrix = self._encoded_matrix

    def get_encoded(self) -> str:
        self._setup()
        self._algorithm()
        self._ASCII_to_char_matrix()
        self._convert_to_string()
        return self._string
    

# decoder
class Decode(Strategy):
    def __init__(self, keyword, string) -> None:
        super().__init__(keyword, string)
        self._decoded_matrix = None

    def _algorithm(self) -> None:
        row = len(self._string_matrix)

        # initialization
        self._decoded_matrix =[ [ 0 for _ in range( len(self._string_matrix[i]) ) ] for i in range(row) ]
        
        for i in range(row):
            for j in range( len(self._string_matrix[i]) ):
                # calculates the difference for decoding
                cache = self._string_matrix[i][j] - self._keyword_matrix[0][ j % len(self._keyword_matrix[0]) ]
                
                if cache < 65:
                    cache += 26
                self._decoded_matrix[i][j] = cache
        self._string_matrix = self._decoded_matrix

    def get_decoded(self) -> str:
        self._setup()
        self._algorithm()
        self._ASCII_to_char_matrix()
        self._convert_to_string()
        return self._string
        

def main():
    encode = Encode("ACT", "BANANA & PEEL")
    encoded_msg = encode.get_encoded()
    print( encoded_msg )

    decode = Decode("ACT", encoded_msg)
    decoded_msg = decode.get_decoded()
    print( decoded_msg)
    


if __name__ == "__main__":
    main()


        # print("keyword matrix: ", self._keyword_matrix)
        # print("string matrix: ", self._string_matrix)
        # print("encoded matrix = ", self._encoded_matrix)