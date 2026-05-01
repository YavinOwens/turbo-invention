from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator
from turbo_invention.models import Document


class SARParser(ABC):
    def __init__(self, root: Path):
        self.root = Path(root)

    @abstractmethod
    def iter_documents(self) -> Iterator[Document]: ...

    @abstractmethod
    def dry_run(self) -> None: ...
