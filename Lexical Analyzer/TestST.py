import SymbolTable as st
import unittest

class TestSymbolTable(unittest.TestCase):

    def test_put_and_get(self):
        table = st.SymbolTable(5)
        table.put("apple")
        table.put("banana")
        table.put("cherry")

        self.assertEqual(table.get("apple"), (0, 0))
        self.assertEqual(table.get("banana"), (4, 0))
        self.assertEqual(table.get("cherry"), (3, 0))

    def test_delete(self):
        table = st.SymbolTable(5)
        table.put("apple")
        table.put("banana")
        table.delete("apple")

        self.assertNotIn("apple", table.data[table._hash_function("apple")])
        self.assertEqual(table.get("banana"), (4, 0))

    def test_get_nonexistent(self):
        table = st.SymbolTable(5)
        self.assertIsNone(table.get("nonexistent"))

if __name__ == '__main__':
    unittest.main()
