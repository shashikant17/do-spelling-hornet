import os.path

import spellchecker


class SpellChecker:
    def __init__(self):
        self.checker = spellchecker.SpellChecker()
        with open(os.path.join(os.path.dirname(__file__),
                               '../dictionaries/custom.txt'), 'r') as cus:
            custom_words = cus.read().splitlines()
            self.checker.word_frequency.load_words(custom_words)

    def find_errors(self, text: str) -> set:
        errors = self.checker.unknown(text.split(" "))
        errors_with_more_than_3_chars = set()
        for error in errors:
            if len(error) > 3:
                errors_with_more_than_3_chars.add(error)
        return errors_with_more_than_3_chars
