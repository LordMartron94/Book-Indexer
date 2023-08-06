import re

from Src.Backend.pipeline import Pipe


class PreProcess(Pipe):
    def pipe(self, data: list[str]) -> list[str]:
        data = self._remove_new_lines(data)
        return self._split_on_dot(data)

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

    def _split_on_dot(self, data):
        output: list[str] = []

        for string in data:
            output.extend(re.split('..', string))

        return output
