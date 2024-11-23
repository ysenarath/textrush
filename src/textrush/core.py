from typing import Dict
from textrush.librush import PyKeywordProcessor


class KeywordProcessor:
    def __init__(self, case_sensitive: bool = False):
        self._kp = PyKeywordProcessor(case_sensitive)

    def add_keyword(self, keyword: str, clean_name: str = None):
        self._kp.add_keyword(keyword, clean_name)

    def add_keywords_from_dict(
        self, dictionary: Dict[str, str], errors: str = "ignore"
    ):
        items = list(dictionary.items())
        try:
            self._kp.add_keywords_with_clean_name_from_iter(items)
        except ValueError as e:
            if errors == "ignore":
                return
            raise e

    def extract_keywords(self, text: str, span_info: bool = False):
        if span_info:
            return self._kp.extract_keywords_with_span(text)
        return self._kp.extract_keywords(text)
