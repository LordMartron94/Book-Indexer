from pathlib import Path

SUPPORTED_FILES: list[str] = [
    ".txt",
    ".pdf",
    ".epub"
]

OUTPUT: Path = Path(__file__).parent.joinpath("Output").absolute()
FILTERS: Path = Path(__file__).parent.joinpath("Src").joinpath("filter_words.txt").absolute()

MODELDATA: Path = Path(__file__).parent.joinpath("Model_Data").absolute()
TESTDATA: Path = Path(__file__).parent.joinpath("Test_Data").absolute()

ROOT: Path = Path(__file__).parent.absolute()
