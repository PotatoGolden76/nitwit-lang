class Grammar:

    def __init__(self, nonterminals, terminals, productions, start) -> None:
        self._nonterminals = nonterminals
        self._terminals = terminals
        self._productions = productions
        self._start = start

    @staticmethod
    def from_file(path):
        nonterminals = []
        terminals = []
        productions = {}
        start = None

        with open(path, 'r') as f:
            nonterminals.extend(f.readline().strip().split(" "))
            terminals.extend(f.readline().strip().split(" "))
            start = f.readline().strip()

            raw_productions = [line.strip() for line in f.readlines()]
            for production in raw_productions:
                lh, rh = production.split('->')

                lh = lh.strip()
                rh = [x.strip() for x in rh.strip().split('|')]

                for alternative in rh:
                    if lh in productions.keys():
                        productions[lh].append(alternative)
                    else:
                        productions[lh] = [alternative]
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

    def is_cfg(self):
        # WTF do i do here????
        pass


if __name__ == "__main__":
    gr = Grammar.from_file("g1.txt")
    print(gr.nonterminals)
    print(gr.terminals)
    print(gr.start)
    print(gr.productions)
    print(gr.get_nonterminal_productions('S'))
    print(gr.get_nonterminal_productions('A'))
    print(gr.get_nonterminal_productions('B'))
    print(gr.get_nonterminal_productions('C'))
    print(gr.get_nonterminal_productions('D'))
    print(gr.is_cfg())
