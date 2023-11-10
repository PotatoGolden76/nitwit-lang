class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.data = [[] for _ in range(size)]

    def __str__(self):
        s = ""
        i = 0
        for line in self.data:
            # if line:
            s += f"{i}:    \t{str(line)}\n"
            i += 1
        s += "\n"
        return s

    def _hash_function(self, token):
        return sum([ord(x) for x in token]) % self.size

    def put(self, token):
        index = self._hash_function(token)
        if token not in self.data[index]:
            self.data[index].append(token)
        return self.get(token)

    def get(self, token):
        index = self._hash_function(token)
        try:
            return index, self.data[index].index(token)
        except:
            return None

    def delete(self, token):
        index = self._hash_function(token)
        self.data[index].remove(token)
