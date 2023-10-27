class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.data = [[] for _ in range(size)]

    def _hash_function(self, token):
        return sum([ord(x) for x in token]) % self.size

    def put(self, token):
        index = self._hash_function(token)
        self.data[index].append(token)

    def get(self, token):
        index = self._hash_function(token)
        try:
            return (index, self.data[index].index(token))
        except:
            return None   

    def delete(self, token):
        index = self._hash_function(token)
        self.data[index].remove(token)

