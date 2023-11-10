import re


def readTokens(file):
    tokens = {}
    with open(file, "r") as f:
        for line in f:
            tokens[line.strip("\n")] = True
    return tokens


def readCode(file):
    tProgram = []
    with open(file, "r") as f:
        tProgram.extend(f.readlines())
    tProgram = [x.strip() for x in tProgram]

    finalProgram = []
    while tProgram:
        if "🗿🗿🗿" in tProgram[0]:
            tProgram.pop(0)
            while "🗿🗿🗿" not in tProgram[0]:
                tProgram.pop(0)
            tProgram.pop(0)
        elif '🗿' in tProgram[0]:
            tProgram.pop(0)
        else:
            finalProgram.append(tProgram[0])
            tProgram.pop(0)
    return [line.split() for line in finalProgram if line != ""]


def separatorSplit(token, separators):
    pattern = f'({"|".join(re.escape(separator) for separator in separators)})'
    return [unit.strip() for unit in re.split(pattern, token) if unit]


def isIdentifier(token):
    pattern = r'^[a-zA-Z][a-zA-Z0-9]*$'
    return bool(re.search(pattern, token))


def isConstant(token):
    numeric_pattern = r'^-?\d+$'
    string_pattern = r'(^"([^"]+)"$)'
    return bool(re.search(numeric_pattern, token) or re.search(string_pattern, token))
