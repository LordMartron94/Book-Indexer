from typing import TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")


class Pipeline(ABC):
    """Abstract pipes class."""

    def flow(self, data: T):
        """To run the pipes."""


class Pipe(ABC):
    @abstractmethod
    def pipe(self, data: T) -> T:
        """Basic pipe method."""
