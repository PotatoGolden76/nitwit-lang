class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def _hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash_function(key)
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append((key, value))

    def get(self, key):
        index = self._hash_function(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        index = self._hash_function(key)
        if self.table[index] is not None:
            for item in self.table[index]:
                if item[0] == key:
                    self.table[index].remove(item)
                    return
        raise KeyError(f"Key '{key}' not found")

# Example usage:
hash_table = HashTable(10)
hash_table.insert("apple", 5)
hash_table.insert("banana", 2)
hash_table.insert("cherry", 8)

print(hash_table.get("apple"))  # Output: 5

hash_table.delete("banana")
