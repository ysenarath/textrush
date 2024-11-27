from __future__ import annotations
import enum
from typing import Dict, Literal
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

    def add_keyword(self, keyword: str, clean_name: str = None):
        self._kp.add_keyword(keyword, clean_name)

    def add_keywords_from_dict(
        self,
        dictionary: Dict[str, str],
        errors: str = "ignore",
    ):
        items = list(dictionary.items())
        try:
            self._kp.add_keywords_with_clean_name_from_iter(items)
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
