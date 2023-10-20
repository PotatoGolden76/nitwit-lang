class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.data = [[] for _ in range(size)]

    def _hash_function(self, key):
        ## TODO: think of a good hash
        pass

    def insert(self, key):
        index = self._hash_function(key)
        if self.data[index] is None:
            self.data[index] = []
        self.data[index].append(key)

    def get(self, key):
        ## TODO: implementation
        pass

    def delete(self, key):
        ## TODO: implementation
        pass