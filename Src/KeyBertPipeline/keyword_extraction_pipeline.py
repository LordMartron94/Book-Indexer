from Src.KeyBertPipeline.extract_key_phrases import ExtractKeyPhrases
from Src.Backend.pipeline import Pipeline
from Src.KeyBertPipeline.preprocess import PreProcess
from Src.KeyBertPipeline.rate_phrases import RatePhrases


class KeywordExtractionPipeline(Pipeline):
    def __init__(self):
        e = ExtractKeyPhrases()
        self._pipeline = [
            PreProcess(),
            e,
            RatePhrases(e.get_vectorizer())
        ]

    def flow(self, data: list[str]):
        for pipe in self._pipeline:
            data = pipe.pipe(data)

        return data
