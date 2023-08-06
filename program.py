import sys
import time

import PyPDF2 as PyPDF2
import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub

from Src.data_manager import DataManager
from Src.KeyBertPipeline.keyword_extraction_pipeline import KeywordExtractionPipeline
from Src.Backend.pipeline import Pipeline
from constants import *


def _verify(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Path: \"{str(path)}\" does not exist!")
    if not path.is_file():
        raise TypeError(f"Path: \"{str(path)}\" is not a file!")
    if path.suffix not in SUPPORTED_FILES:
        raise AttributeError(f"File: \"{str(path)}\" is not a supported file type!\nType given: "
                             f"\"{path.suffix}\"")


class Program:
    def __init__(self):
        self._file_path = self._get_file_path()

        top = int(input("How many top keywords do you want to get?\n>>> "))

        self._data_manager: DataManager = DataManager(self._file_path, top)

        self._pipeline: Pipeline = KeywordExtractionPipeline()

    def _get_file_path(self) -> Path:
        if len(sys.argv) > 1:
            path: Path = Path(sys.argv[1])
            _verify(path)
            return path

        path: Path = Path(input("What is the path of the file you want to index? "))

        try:
            _verify(path)
            return path
        except Exception as e:
            print(e)
            time.sleep(0.5)
            return self._get_file_path()

    def main(self):
        if self._file_path.suffix == ".txt":
            self._handle_text()
        elif self._file_path.suffix == ".pdf":
            self._handle_pdf()
        elif self._file_path.suffix == ".epub":
            self._handle_epub()

    def _handle_text(self):
        ...

    def _handle_pdf(self):
        pdf_file_obj = open(self._file_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)

        texts: list[str] = []

        for page in pdf_reader.pages:
            texts.append(page.extract_text())

        output: list[list[tuple[str, float]]] = self._pipeline.flow(texts)

        self._data_manager.save_output(output)

    def _chapter_to_str(self, chapter):
        soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
        text = [para.get_text() for para in soup.find_all('p')]
        return ' '.join(text)

    def _handle_epub(self):
        book = epub.read_epub(self._file_path)
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

        texts = {}
        for c in items:
            texts[c.get_name()] = self._chapter_to_str(c)

        content: list[str] = []

        for chapter_name, chapter_content in texts.items():
            content.append(chapter_content)

        output: list[list[tuple[str, float]]] = self._pipeline.flow(content)

        self._data_manager.save_output(output)


if __name__ == "__main__":
    Program().main()
