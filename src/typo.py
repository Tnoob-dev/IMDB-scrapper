from yarl import URL
from typing import NamedTuple, List, Tuple

class ResultReturned(NamedTuple):
    name: str
    url: URL
    
class FinalResult(NamedTuple):
    title: str
    original_title: str
    duration: str
    synopsis: str
    genres: List[str]