import pickle
import pprint

from keras import Sequential
from keras.layers import LSTM, Dense, TimeDistributed, Flatten
from numpy import ndarray
from numpy._typing import ArrayLike

from Src.Backend.vocabulary_manager import VocabularyManager
from Src.InitialEmbedder import InitialEmbedder
from constants import TESTDATA, MODELDATA

import numpy as np


class Test:
    def __init__(self):
        self._max_par_tokens: int = 250
        self._max_output_keywords: int = 5
        self._model: Sequential = self._create_model()

    def _create_model(self) -> Sequential:
        # Create Layers
        model = Sequential()

        lstm = LSTM(units=1, input_shape=(self._max_par_tokens, 1), return_sequences=True)
        model.add(lstm)

        # The input shape of the TimeDistributed layer should be based on the output of the LSTM layer
        # Which should be (batch_size, self._max_par_tokens, units)
        model.add(TimeDistributed(Dense(4, activation='ReLU')))
        model.compile()

        return model

    def _train_model(self):
        self._model.fit()

    def run(self):
        lines: list[str] = []

        with open(TESTDATA.joinpath('CLT.txt')) as file:
            lines = file.readlines()

        input_sample = self._build_paragraph_embedding(par_txt=lines, max_tokens=self._max_par_tokens)
        output_sample = self._build_output_embedding(output=
                                                     ["information",
                                                      "memory",
                                                      "generation effect",
                                                      "context memory",
                                                      "generation tasks"])

        self._model.fit(input_sample, output_sample, 100)
        pickle.dump(self._model, open(MODELDATA.joinpath('model.sav'), 'wb'))

        pprint.pprint(self._model.predict(input_sample))

    def _build_paragraph_embedding(self, par_txt: list[str], max_tokens: int):
        vocab_mgr = VocabularyManager()
        embedder = InitialEmbedder(vocab_mgr)

        arr = np.array([i for sublist in [embedder.embed(sentence) for sentence in par_txt] for i in sublist])
        if arr.shape[0] < max_tokens:
            arr = np.append(arr, [-1 for _ in range(arr.shape[0], max_tokens)])

        return arr

    def _build_output_embedding(self, output: list[str]):
        vocab_mgr = VocabularyManager()
        embedder = InitialEmbedder(vocab_mgr)

        tokens = [embedder.embed(sentence) for sentence in output]

        i = -1

        for t in tokens:
            i += 1

            if len(t) < 4:
                t.extend([-1 for _ in range(len(t), 4)])
                tokens[i] = t
                print(t)

        arr = np.stack(tokens)
        return arr

    def _reverse_lookup(self, words):
        vocab_mgr = VocabularyManager()

        for word in words:
            w = vocab_mgr.reverse_lookup(word)[0]
            print(w)


if __name__ == "__main__":
    Test().run()
