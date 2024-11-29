from __future__ import annotations
import enum
from typing import Literal, Iterable, List, Mapping, Tuple
from textrush.librush import PyKeywordProcessor
import operator as op

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

    def remove_keywords_from_list(self, keywords: List[str]):
        for word in keywords:
            self._kp.remove_keyword(word)

    def remove_keywords_from_dict(
        self,
        mapping: Mapping[str, Iterable[str] | str],
    ):
        values: List[str] = []
        for _, value in mapping.items():
            if isinstance(value, str):
                values.append(value)
                continue
            values.extend(value)
        for word in values:
            self._kp.remove_keyword(word)

    def add_keyword(self, keyword: str, clean_name: str = None):
        self._kp.add_keyword(keyword, clean_name)

    def add_keywords_from_iter(self, keywords: Iterable[Tuple[str, str] | str]):
        for keyword in keywords:
            if isinstance(keyword, str):
                self._kp.add_keyword(keyword)
            else:
                self._kp.add_keyword(*keyword)

    def add_keywords_from_dict(
        self,
        mapping: Mapping[str, Iterable[str] | str],  # clean_name: [keyword1, keyword2]
        errors: str = "raise",
    ):
        if errors not in ("raise", "ignore"):
            raise ValueError(
                f"invalid value for errors: {errors}. "
                "Must be one of 'raise', 'ignore'."
            )
        for clean_name, keywords in mapping.items():
            if isinstance(keywords, str):
                keywords = [keywords]
                continue
            for word in keywords:
                try:
                    self._kp.add_keyword(word, clean_name)
                except ValueError as e:
                    if errors == "ignore":
                        return
                    raise e

    def extract_keywords(
        self,
        text: str,
        span_info: bool = False,
        strategy: ExtractorStrategy
        | Literal["all", "longest", "ALL", "LONGEST"] = ExtractorStrategy.ALL,
    ):
        if isinstance(strategy, ExtractorStrategy):
            strategy = strategy.name.lower()
        if span_info:
            return self._kp.extract_keywords_with_span(text, strategy=strategy)
        return self._kp.extract_keywords(text, strategy=strategy)

    def replace_keywords(self, text: str) -> str:
        return self._kp.replace_keywords(text)

    def get_all_keywords_with_clean_names(self) -> List[Tuple[str, str]]:
        return self._kp.get_all_keywords_with_clean_names()

    def get_all_keywords(self) -> List[str]:
        return list(
            map(
                op.itemgetter(0),
                self._kp.get_all_keywords_with_clean_names(),
            )
        )

    def __len__(self):
        return len(self._kp)
