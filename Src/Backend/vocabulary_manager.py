from typing import List

from Src.Backend.json_handling import JsonStorage
from Src.Backend.preprocessor import Preprocessor
from Src.Backend.vocabulary import Vocabulary
from constants import MODELDATA, ROOT


class VocabularyManager:
    def __init__(self):
        self._preprocessor = Preprocessor()
        self._storage = JsonStorage(ROOT, "Model_Data")
        self._vocab: [Vocabulary, None] = None
        self._vocab = self.get_vocabulary()

    def fit_vocabulary_on_text(self, text: str) -> None:
        words: List[str] = self._preprocessor.preprocess_text(text)

        for word in words:
            self._vocab.add_item(word)

    def get_vocabulary(self) -> Vocabulary:
        if MODELDATA.joinpath('vocabulary.json').exists() and self._vocab is None:
            return Vocabulary.parse_file(MODELDATA.joinpath('vocabulary.json'), content_type='json')
        elif self._vocab is None:
            return Vocabulary(contents=[])

        return self._vocab

    def save_vocabulary(self):
        js: dict = self._vocab.dict()
        self._storage.write_json_file(js, "vocabulary.json")

    def word_lookup(self, word: str) -> tuple[int, int]:
        """

        :param word: The word to look up.
        :return: A tuple where the first element is the index, and the second element the occurrence number.
        """
        for c in self._vocab.contents:
            if c.word == word:
                return c.index, c.occurrences

    def reverse_lookup(self, word: int):
        for c in self._vocab.contents:
            if c.index == word:
                return c.word, c.occurrences
