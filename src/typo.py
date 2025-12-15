from yarl import URL
from typing import NamedTuple, List
from pathlib import Path

class ResultReturned(NamedTuple):
    name: str
    url: URL
    
class FinalResult(NamedTuple):
    title: str
    original_title: str
    duration: str
    synopsis: str
    score: float
    image_path: Path
    genres: List[str]