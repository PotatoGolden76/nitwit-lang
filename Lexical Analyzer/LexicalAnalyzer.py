import os
from SymbolTable import SymbolTable
from InternalForm import ProgramInternalForm
from Utils import *


class Scanner:
    def __init__(self):
        self._identifierTable = SymbolTable(size=15)
        self._constantTable = SymbolTable(size=15)
        self._PIF = ProgramInternalForm()

        self._lastScan = ""

        self.operators = {}
        self.separators = {}
        self.reserved = {}
        self.identifiers = {}
        self.alphabet = {}

        self.loadCompilerData()

    @property
    def PIF(self):
        return self._PIF

    @property
    def IT(self):
        return self._identifierTable

    @property
    def CT(self):
        return self._constantTable

    def loadCompilerData(self):
        self.reserved = readTokens("Compiler Data/reserved.in")
        self.separators = readTokens("Compiler Data/separators.in")
        self.operators = readTokens("Compiler Data/operators.in")
        self.alphabet = readTokens("Compiler Data/token.in")

    def error(self, token):
        if self._lastScan:
            with open(self._lastScan, "r") as f:
                for number, line in enumerate(f):
                    if token in line:
                        raise SyntaxError(f"Unknown token '{token}' in file '{self._lastScan}', on line {number}")

    def scan(self, file):
        self._lastScan = file
        tokens = readCode(file)
        tokens = [x for sublist in tokens for x in sublist]

        while tokens:
            current = tokens[0]
            tokens.pop(0)

            if self.isSTToken(current):
                self.PIF.add(current, -1)
            elif isConstant(current) or isIdentifier(current):
                self.registerTokens(current)
            else:
                try:
                    t = self.splitToken(current)
                except SyntaxError as e:
                    print(e)
                    break
                tokens = t + tokens  # add to the beginning the new tokens

        if not tokens:
            self.printST()
            with open("Output/PIF.out", "w") as g:
                g.write(str(self.PIF))
        print("Scan successful")

    def splitToken(self, token):
        tokenUnits = separatorSplit(token, list(self.separators.keys()))
        if len(tokenUnits) <= 1:
            tokenUnits = separatorSplit(token, list(self.operators.keys()))
        if len(tokenUnits) <= 1:
            self.error(token)
        return tokenUnits

    def isSTToken(self, token):
        return (token in self.separators.keys() or token in self.operators.keys() or
                token in self.reserved.keys() or token in self.alphabet.keys())

    def registerTokens(self, token):
        pos = -1
        if isIdentifier(token):
            pos = self._identifierTable.put(token)
        elif isConstant(token):
            pos = self._constantTable.put(token)
        self.PIF.add(token, pos)

    def printST(self):
        with open("Output/identifier_table.out", "w") as g:
            g.write(str(self.IT))

        with open("Output/constant_table.out", "w") as g:
            g.write(str(self.CT))


if __name__ == "__main__":
    scanner = Scanner()
    scanner.scan("/home/roberthara/Desktop/nitwit-lang/Examples/Lab 1a/perr.npl")
