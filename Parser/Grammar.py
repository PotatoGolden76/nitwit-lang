class Grammar:

    def __init__(self, nonterminals, terminals, productions, start) -> None:
        self._nonterminals = nonterminals
        self._terminals = terminals
        self._productions = productions
        self._start = start

    # This static functions takes in a file path and returns a Grammar object from the data in the file
    # -> it starts by reading the nonterminals, terminals, and the start object, because each of them 
    # is situated on a single line
    # -> it proceeds by processing all of the remaining lines and paring them into productions

    @staticmethod
    def from_file(path):
        nonterminals = []
        terminals = []
        productions = {}
        start = None

        with open(path, 'r') as f:
            # Read the single-line elements
            nonterminals.extend(f.readline().strip().split(" "))
            terminals.extend(f.readline().strip().split(" "))
            start = f.readline().strip()

            # process all of the remaining lines
            raw_productions = [line.strip() for line in f.readlines()]
            for production in raw_productions:
                # spilt the current line in left hand and right hand sides
                lh, rh = production.split('->')

                lh = lh.strip()
                # split the right hand side in variations
                rh = [x.strip() for x in rh.strip().split('|')]

                # add each variation to the list of productions
                for alternative in rh:
                    if lh in productions.keys():
                        productions[lh].append(alternative)
                    else:
                        productions[lh] = [alternative]
        # Return the Grammar object
        return Grammar(nonterminals, terminals, productions, start)

    @property
    def nonterminals(self):
        return self._nonterminals

    @property
    def terminals(self):
        return self._terminals

    @property
    def start(self):
        return self._start

    @property
    def productions(self):
        return self._productions

    def get_nonterminal_productions(self, nonterminal):
        if nonterminal in self._productions:
            return self._productions[nonterminal]
        return []


     # With this method we check if a grammar is a context free grammar
     # -> First we check if the starting symbols is found within the non-terminals
     # -> Second we check if on the left hand side we have only one non-terminal (for each production)
     # -> Third we check if the productions of that left hand side non-terminal can be found within the non-terminals set or terminals set or is equal to the empty sequence
    
    def is_cfg(self):
        # Check if the start symbol is a non-terminal
        if self._start not in self._nonterminals:
            print(f"Start symbol {self._start} is not a non-terminal.")
            return False

        # Check each production
        for lh, rhs_list in self._productions.items():
            # Left-hand side should be a single non-terminal
            if lh not in self._nonterminals:
                print(f"Left-hand side {lh} is not a non-terminal.")
                return False

            # Check right-hand side of the productions
            for rhs in rhs_list:
                # Split the right-hand side into individual tokens
                rhs_symbols = rhs.split(" ")

                # Check each symbol in the right-hand side
                for symbol in rhs_symbols:
                    if symbol not in self._terminals and symbol not in self._nonterminals:
                        print(f"Symbol {symbol} in production {lh} -> {rhs} is neither a terminal nor a non-terminal.")
                        return False

        return True


if __name__ == "__main__":
    gr = Grammar.from_file("g1.txt")
    print(gr.nonterminals)
    print()
    print(gr.terminals)
    print()
    print(gr.start)
    print()
    for key in gr.productions:
        print(f"{key} -> {gr.productions[key]}\n")

    print(gr.is_cfg())