import re


class Preprocessor:
    def preprocess_text(self, text: str) -> list[str]:
        b = [text]
        output = self._remove_new_lines(b)

        for word in output:
            output[output.index(word)] = word.lower()

        output = self._separate_words_and_punctuation(output)
        return output

    def _remove_new_lines(self, body: list[str]):
        removed: list[str] = []

        for body_part in body:
            new = ""
            for i in range(len(body_part)):
                if body_part[i] == "\n" and i > 0 and body_part[i-1] == "-":
                    new += ""
                elif body_part[i] == "\n":
                    new += " "
                else:
                    new += body_part[i]
            removed.append(new)

        return removed

    def _separate_words_and_punctuation(self, text: list[str]):
        # Use regular expression to separate out words and punctuation and keep them in sequence
        words = []

        for t in text:
            words.extend(re.finditer(r'\b[\w.-]+\b|[^\s\w.-]', t))

        return [word.group() for word in words]


