from keyphrase_vectorizers import KeyphraseCountVectorizer

from Src.Backend.pipeline import Pipe


class ExtractKeyPhrases(Pipe):
    def __init__(self):
        self._vectorizer = KeyphraseCountVectorizer()

    def pipe(self, body: list[str]) -> list[str]:
        self._vectorizer.fit_transform(body)
        o = self._vectorizer.get_feature_names_out()
        return o

    def get_vectorizer(self):
        return self._vectorizer
