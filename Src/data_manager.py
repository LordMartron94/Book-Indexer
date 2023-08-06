from pathlib import Path

from constants import OUTPUT


class DataManager:
    def __init__(self, file_path: Path, top):
        self._top = top
        self._file_path: Path = file_path

    def save_output(self, output: list[list[tuple[str, float]]]):
        with open(OUTPUT.joinpath(self._file_path.name + ".txt"), 'w', encoding='utf-8') as output_file:
            lines: list[str] = []
            keyphrase_dict = {}

            for topic in output:
                for keyphrase, value in topic:
                    if keyphrase in keyphrase_dict:
                        keyphrase_dict[keyphrase] += value
                    else:
                        keyphrase_dict[keyphrase] = value

            sorted_keyphrases = sorted(keyphrase_dict.items(), key=lambda x: x[1], reverse=True)

            for i, (keyphrase, value) in enumerate(sorted_keyphrases):
                if i >= self._top:
                    break
                lines.append(f"{keyphrase}: {value}\n")

            output_file.writelines(lines)


