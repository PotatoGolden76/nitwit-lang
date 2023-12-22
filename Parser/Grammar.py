from texttable import Texttable


class ParseTreeNode:
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children if children is not None else []

    def add_child(self, node):
        self.children.append(node)


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
                    if symbol not in self._terminals and symbol not in self._nonterminals and symbol != 'ε':
                        print(f"Symbol {symbol} in production {lh} -> {rhs} is neither a terminal nor a non-terminal.")
                        return False

        return True

    def is_terminal(self, symbol):
        return symbol in self._terminals

    def is_nonterminal(self, symbol):
        return symbol in self._nonterminals


    def compute_first(self, symbol):
        first_set = set()

        if self.is_terminal(symbol):
            first_set.add(symbol)
        elif self.is_nonterminal(symbol):
            productions = self.get_nonterminal_productions(symbol)

            for production in productions:
                rhs_symbols = production.split(" ")
                first_set.update(self.compute_first(rhs_symbols[0]))

        return first_set


    def compute_follow(self, nonterminal, computed=None):
        if computed is None:
            computed = set()

        follow_set = set()

        if nonterminal == self._start:
            follow_set.add('$')  # $ - end of input

        computed.add(nonterminal)

        for lh, rhs_list in self._productions.items():
            for rhs in rhs_list:
                rhs_symbols = rhs.split(" ")

                if nonterminal in rhs_symbols:
                    index = rhs_symbols.index(nonterminal)

                    if index < len(rhs_symbols) - 1:
                        next_symbol = rhs_symbols[index + 1]

                        if next_symbol in self._nonterminals:
                            if next_symbol not in computed:
                                follow_set.update(self.compute_follow(next_symbol, computed))

                            # Include first of the symbol after nonterminal in Follow set
                            follow_set.update(self.compute_first(next_symbol))

                            # Include epsilon in Follow set if everything after A is epsilon
                            if 'ε' in self.compute_first(next_symbol):
                                follow_set.update(self.compute_follow(lh, computed))

                        elif next_symbol in self._terminals:
                            follow_set.add(next_symbol)

                    elif lh != nonterminal:
                        if lh not in computed:
                            follow_set.update(self.compute_follow(lh, computed))

                    elif 'ε' in self.compute_first(nonterminal):
                        # Include epsilon in Follow set for the current nonterminal
                        follow_set.update(self.compute_follow(lh, computed))

        return follow_set
    

    def generate_parsing_table(self):
        if not self.is_cfg():
            print("Cannot generate parsing table for non-context-free grammar.")
            return None

        # Initialize the parsing table as a dictionary
        parsing_table = {}

        # Initialize table entries for each nonterminal and terminal to an empty string
        for nonterminal in self._nonterminals:
            for terminal in self._terminals + ['$']:  # Include the end-of-input symbol
                parsing_table[(nonterminal, terminal)] = ""  # Use empty string instead of None

        # Populate the parsing table
        for nonterminal in self._nonterminals:
            for production in self.get_nonterminal_productions(nonterminal):
                # Compute FIRST of the right-hand side of the production
                symbols = production.split()

                for symbol in symbols:
                    first_set = self.compute_first(symbol)  # Assuming compute_first works for both terminals and non-terminals

                    for terminal in first_set:
                        if terminal != 'ε':  # If epsilon is not in FIRST, add the production
                            parsing_table[(nonterminal, terminal)] = production

                    # If ε is in FIRST or production is ε, add the production for all terminals in FOLLOW(nonterminal)
                    if 'ε' in first_set or production == 'ε':
                        follow_set = self.compute_follow(nonterminal)
                        for follow_terminal in follow_set:
                            # Add the production to the parsing table if the cell is empty or contains an epsilon production
                            if not parsing_table[(nonterminal, follow_terminal)] or 'ε' in parsing_table[(nonterminal, follow_terminal)]:
                                parsing_table[(nonterminal, follow_terminal)] = production

                    # If the symbol is a non-terminal and leads to ε, continue to the next symbol
                    if 'ε' in first_set and symbol != symbols[-1]:
                        continue
                    else:
                        break  # Break out of the loop if we've found a non-ε production or reached the end of the production

        # Return the parsing table
        return parsing_table
    

    def ll1_parser(self, input_string):
        input_string += '$'
        input_tokens = [c for c in input_string]

        root = ParseTreeNode(self._start)  # Root of the parse tree
        stack = [('$', None), (self._start, root)]  # Stack holds tuples of (symbol, tree_node)

        input_pointer = 0
        parsing_table = self.generate_parsing_table()

        while len(stack) > 1:  # The stack will always contain the end symbol '$'
            stack_top, tree_node = stack[-1]
            current_input = input_tokens[input_pointer]

            if stack_top == current_input:
                if stack_top == '$':
                    return True, root  # Successful parsing and return root of the parse tree
                else:
                    stack.pop()
                    input_pointer += 1
            else:
                rule = parsing_table.get((stack_top, current_input))
                if rule:
                    stack.pop()  # Pop the nonterminal
                    children = []

                    if rule != 'ε':
                        for symbol in reversed(rule.split()):
                            child_node = ParseTreeNode(symbol)
                            children.append(child_node)
                            stack.append((symbol, child_node))

                    tree_node.children = children  # Attach children to the current node
                else:
                    return False, None  # Parsing error

        return True, root  # Return the success status and the parse tree root



    def print_parsing_table(self):
        parsing_table = self.generate_parsing_table()
        if parsing_table is None:
            return

        table = Texttable()
        table.add_row([''] + self._terminals + ['$'])

        for nonterminal in self._nonterminals:
            row = [nonterminal]
            for terminal in self._terminals + ['$']:
                entry = parsing_table.get((nonterminal, terminal), '')
                row.append(entry)
            table.add_row(row)

        print(table.draw())


def print_tree(node, indent="", last=True):
    prefix = "└── " if last else "├── "
    print(indent + prefix + node.symbol)
    indent += "    " if last else "│   "
    for i, child in enumerate(node.children):
        last_child = i == (len(node.children) - 1)  # Check if it's the last child
        print_tree(child, indent, last_child)

if __name__ == "__main__":
    gr = Grammar.from_file("./g1.txt")
    print("Nonterminals: ", gr.nonterminals)
    # print()
    print("Terminals: ", gr.terminals)
    # print()
    print("Start: ", gr.start)
    print("Productions:")
    for key in gr.productions:
        print(f"{key} -> {gr.productions[key]}")
    print()

    print("FIRST: ")
    for nt in gr.nonterminals:
        print(gr.compute_first(nt))
    print()
    print("FOLLOW: ")
    for nt in gr.nonterminals:
        print(gr.compute_follow(nt))

    print()
    # gr.print_parsing_table()
    gr.print_parsing_table()

    input_string = input("Input String: ")
    success, parse_tree_root = gr.ll1_parser(input_string)

    if success:
        print("Parsing successful! Here's the parse tree:")
        print_tree(parse_tree_root)
    else:
        print("Parsing failed.")
