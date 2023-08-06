from keybert import KeyBERT

from Src.Backend.pipeline import Pipe


class RatePhrases(Pipe):
    def __init__(self, vectorizer):
        self._vectorizer = vectorizer
        self._model = KeyBERT()

    def pipe(self, data: list[str]) -> list[list[tuple[str, float]]]:
        return self._model.extract_keywords(docs=data, vectorizer=self._vectorizer, top_n=5)
