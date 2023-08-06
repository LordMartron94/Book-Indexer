from typing import List

import pydantic


class WordContent(pydantic.BaseModel):
    word: str
    occurrences: int
    index: int


class Vocabulary(pydantic.BaseModel):
    contents: List[WordContent]

    def add_item(self, content: str):
        if self._item_exists(content):
            i = self._get_index(content)

            if i == -1:
                raise Exception("Something went wrong!")

            self.contents[i].occurrences += 1
            return

        index: int = len(self.contents) + 1

        self.contents.append(WordContent(word=content, occurrences=1, index=index))

    def _item_exists(self, word: str) -> bool:
        for c in self.contents:
            if c.word == word:
                return True

        return False

    def _get_index(self, word: str) -> int:
        for c in self.contents:
            if c.word == word:
                return c.index - 1

        return -1
