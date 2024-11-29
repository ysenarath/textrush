from __future__ import annotations
import enum
from typing import Dict, Literal, Iterable, List, Tuple
from textrush.librush import PyKeywordProcessor

__all__ = [
    "KeywordProcessor",
]


class ExtractorStrategy(enum.Enum):
    ALL = 0
    LONGEST = 1


class KeywordProcessor:
    def __init__(self, case_sensitive: bool = False):
        self._kp = PyKeywordProcessor(case_sensitive)

    def remove_keyword(self, keyword: str):
        self._kp.remove_keyword(keyword)

    def remove_keywords_from_dict(self, dictionary: Dict[str, Iterable[str] | str]):
        values: List[str] = []
        for _, value in dictionary.items():
            if isinstance(value, str):
                values.append(value)
                continue
            values.extend(value)
        for word in values:
            self._kp.remove_keyword(word)

    def add_keyword(self, keyword: str, clean_name: str = None):
        self._kp.add_keyword(keyword, clean_name)

    def add_keywords_from_dict(
        self,
        dictionary: Dict[str, Iterable[str] | str],  # clean_name: word
        errors: str = "ignore",
    ):
        keywords: list[tuple[str, str]] = []  # keyword, clean_name
        for clean_name, keyword in dictionary.items():
            if isinstance(keyword, str):
                keywords.append((keyword, clean_name))
                continue
            for word in keyword:
                keywords.append((word, clean_name))
        try:
            self._kp.add_keywords_with_clean_name_from_iter(iter(keywords))
        except ValueError as e:
            if errors == "ignore":
                return
            raise e

    def extract_keywords(
        self,
        text: str,
        span_info: bool = False,
        strategy: ExtractorStrategy | Literal["all", "longest"] | None = None,
    ):
        if strategy is None:
            strategy = ExtractorStrategy.ALL
        if isinstance(strategy, ExtractorStrategy):
            strategy = strategy.name.lower()
        if span_info:
            return self._kp.extract_keywords_with_span(text, strategy=strategy)
        return self._kp.extract_keywords(text, strategy=strategy)

    def replace_keywords(self, text: str) -> str:
        return self._kp.replace_keywords(text)

    def get_all_keywords(self) -> List[Tuple[str, str]]:
        return self._kp.get_all_keywords()

    def __len__(self):
        return len(self._kp)
