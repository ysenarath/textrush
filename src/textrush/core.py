from textrush.librush import PyKeywordProcessor


class KeywordProcessor:
    def __init__(self, case_sensitive: bool = False):
        self._kp = PyKeywordProcessor(case_sensitive)

    def add_keyword(self, keyword: str, clean_name: str = None):
        self._kp.add_keyword(keyword, clean_name)

    def extract_keywords(self, text: str, span_info: bool = False):
        if span_info:
            return self._kp.extract_keywords_with_span(text)
        return self._kp.extract_keywords(text)
