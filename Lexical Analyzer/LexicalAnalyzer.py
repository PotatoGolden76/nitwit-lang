from SymbolTable import SymbolTable

# 1b  separate tables for identifiers, respectively 
#   Constants (create 2 instances)
# Symbol Table (you need to implement the data structure and required operations) :

"""
While (not(eof)) do
    detect(token);
    if token is reserved word OR operator OR separator
        then genPIF(token, 0)
    else 
        if token is identifier OR constant
            then index = pos(token, ST);
            genPIF(token_type, index)
        else 
            message “Lexical error”
        endif
    endif
endwhile
"""

class Scanner: 
    def __init__(self, input) -> None:
        self._input_file = input