from typing import List

from Src.Backend.preprocessor import Preprocessor
from Src.Backend.vocabulary_manager import VocabularyManager


class InitialEmbedder:
    def __init__(self, vocab_manager: VocabularyManager):
        self._vocab_manager: VocabularyManager = vocab_manager
        self._processor: Preprocessor = Preprocessor()

    def embed(self, text: str) -> List[int]:
        self._vocab_manager.fit_vocabulary_on_text(text)
        self._vocab_manager.save_vocabulary()

        tokens: list[str] = self._processor.preprocess_text(text)

        embedded: list[int] = []

        for t in tokens:
            index: int = self._vocab_manager.word_lookup(t)[0]
            embedded.append(index)

        return embedded
