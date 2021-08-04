import unittest

from src.spell_checker import SpellChecker


class SpellCheckTestCase(unittest.TestCase):
    def test_sentence_spelling(self):
        checker = SpellChecker()
        errors = checker.find_errors("A quik brown fox jmped over the laxy dog")
        self.assertEqual({"quik", "jmped", "laxy"}, errors)


if __name__ == '__main__':
    unittest.main()
