from textrush import KeywordProcessor
import logging
import unittest
import json

logger = logging.getLogger(__name__)


class TestKeywordRemover(unittest.TestCase):
    def setUp(self):
        logger.info("Starting...")
        with open("tests/keyword_remover_test_cases.json") as f:
            self.test_cases = json.load(f)

    def tearDown(self):
        logger.info("Ending.")

    def test_remove_keywords(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Remove the keywords in remove_keyword_dict
        Extract keywords and check if they match the expected result for the test case.
        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor()
            keyword_processor.add_keywords_from_dict(test_case["keyword_dict"])
            keyword_processor.remove_keywords_from_dict(
                test_case["remove_keyword_dict"]
            )
            keywords_extracted = keyword_processor.extract_keywords(
                test_case["sentence"], strategy="longest"
            )
            self.assertEqual(
                keywords_extracted,
                test_case["keywords"],
                "keywords_extracted don't match the expected results for test case: {}".format(
                    test_id
                ),
            )

    def test_remove_keywords_using_list(self):
        """For each of the test case initialize a new KeywordProcessor.
        Add the keywords the test case to KeywordProcessor.
        Remove the keywords in remove_keyword_dict
        Extract keywords and check if they match the expected result for the test case.
        """
        for test_id, test_case in enumerate(self.test_cases):
            keyword_processor = KeywordProcessor()
            keyword_processor.add_keywords_from_dict(test_case["keyword_dict"])
            for key in test_case["remove_keyword_dict"]:
                keyword_processor.remove_keywords_from_iter(
                    test_case["remove_keyword_dict"][key]
                )
            keywords_extracted = keyword_processor.extract_keywords(
                test_case["sentence"], strategy="longest"
            )
            self.assertEqual(
                keywords_extracted,
                test_case["keywords"],
                "keywords_extracted don't match the expected results for test case: {}".format(
                    test_id
                ),
            )


if __name__ == "__main__":
    unittest.main()
