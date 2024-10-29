from typing import Optional, Iterable, Union, List, Tuple, TypeVar, overload
from textrush.librush import KeywordProcessor as BaseKeywordProcessor

__all__ = [
    "KeywordProcessor",
]

T = TypeVar("T", str, Iterable[str])


class KeywordProcessor:
    """Fast keyword extraction and replacement using Aho-Corasick algorithm."""

    def __init__(self, case_sensitive: bool = False) -> None:
        """Initialize KeywordProcessor.

        Parameters
        ----------
        case_sensitive : bool, optional
            Whether to perform case-sensitive matching, by default False
        """
        self._processor = BaseKeywordProcessor(case_sensitive)

    def __len__(self) -> int:
        return len(self._processor)

    def __repr__(self) -> str:
        return repr(self._processor)

    def add_keyword(self, word: str, clean_word: Optional[str] = None) -> None:
        """Add a keyword to the processor.

        Parameters
        ----------
        word : str
            Keyword to add
        clean_word : str, optional
            Clean version of the word to return when found, by default None
            If None, returns the original word
        """
        self._processor.add_keyword(word, clean_word)

    def add_keywords_from_iter(self, words: Iterable[str]) -> None:
        """Add multiple keywords from an iterator.

        Parameters
        ----------
        words : Iterable[str]
            Iterator of keywords to add
        """
        self._processor.add_keywords_from_iter(words)

    def add_keywords_with_clean_word_from_iter(
        self, words: Iterable[tuple[str, str]]
    ) -> None:
        """Add multiple keywords with their clean versions from an iterator.

        Parameters
        ----------
        words : Iterable[tuple[str, str]]
            Iterator of (word, clean_word) tuples
        """
        self._processor.add_keywords_with_clean_word_from_iter(words)

    @overload
    def extract_keywords(
        self, text: str, *, span_info: bool = False
    ) -> Union[
        List[str],  # when span_info=False
        List[Tuple[str, int, int]],  # when span_info=True
    ]: ...

    @overload
    def extract_keywords(
        self, text: Iterable[str], *, span_info: bool = False
    ) -> Union[
        List[List[str]],  # when span_info=False
        List[List[Tuple[str, int, int]]],  # when span_info=True
    ]: ...

    def extract_keywords(
        self, text: Union[str, Iterable[str]], *, span_info: bool = False
    ) -> Union[
        List[str],  # single text, no spans
        List[Tuple[str, int, int]],  # single text, with spans
        List[List[str]],  # multiple texts, no spans
        List[List[Tuple[str, int, int]]],  # multiple texts, with spans
    ]:
        """Extract keywords from text(s).

        Parameters
        ----------
        text : Union[str, Iterable[str]]
            Either a single string or an iterable of strings to extract keywords from
        span_info : bool, optional
            Whether to include position information, by default False

        Returns
        -------
        Union[List[str], List[Tuple[str, int, int]], List[List[str]], List[List[Tuple[str, int, int]]]]
            For single text:
                - If span_info=False: List[str]
                    List of found keywords
                - If span_info=True: List[Tuple[str, int, int]]
                    List of tuples (keyword, start_index, end_index)
            For multiple texts:
                - If span_info=False: List[List[str]]
                    List of lists of found keywords
                - If span_info=True: List[List[Tuple[str, int, int]]]
                    List of lists of tuples (keyword, start_index, end_index)

        Examples
        --------
        >>> kp = KeywordProcessor()
        >>> kp.add_keywords_from_iter(['python', 'rust'])

        # Single text
        >>> kp.extract_keywords('I love python and rust')
        ['python', 'rust']
        >>> kp.extract_keywords('I love python and rust', span_info=True)
        [('python', 7, 13), ('rust', 18, 22)]

        # Multiple texts
        >>> texts = ['python code', 'rust code']
        >>> kp.extract_keywords(texts)
        [['python'], ['rust']]
        >>> kp.extract_keywords(texts, span_info=True)
        [[('python', 0, 6)], [('rust', 0, 4)]]
        """
        if isinstance(text, str):
            if span_info:
                return self._processor.extract_keywords_with_span(text)
            return self._processor.extract_keywords(text)
        else:
            if span_info:
                return self._processor.extract_keywords_with_span_from_list(text)
            return self._processor.extract_keywords_from_list(text)

    def replace_keywords(self, text: str) -> str:
        """Replace keywords in text with their clean versions.

        Parameters
        ----------
        text : str
            Text to replace keywords in

        Returns
        -------
        str
            Text with keywords replaced by their clean versions

        Examples
        --------
        >>> kp = KeywordProcessor()
        >>> kp.add_keyword('python', 'Python')
        >>> kp.replace_keywords('I love python')
        'I love Python'
        """
        return self._processor.replace_keywords(text)
