use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[path = "."]
pub mod case_insensitive {
    use std::collections::hash_map::Entry;
    use unicase::UniCase;

    #[derive(Debug, Default, PartialEq)]
    struct UnicaseHashMap<'a, V> {
        inner: std::collections::HashMap<UniCase<&'a str>, V, fxhash::FxBuildHasher>,
    }

    impl<'a, V> UnicaseHashMap<'a, V> {
        pub fn entry(&mut self, k: &'a str) -> Entry<UniCase<&'a str>, V> {
            // TODO: make sure its not doing the ASCII check
            // TODO: benchmark `into() vs Unicase::unicode()`
            self.inner.entry(UniCase::unicode(k))
        }

        pub fn get(&self, k: &'a str) -> Option<&V> {
            self.inner.get(&UniCase::unicode(k))
        }
    }

    type HashMap<'a, Node> = UnicaseHashMap<'a, Node>;
    mod shared;
    pub use shared::KeywordProcessor;
}

#[path = "."]
pub mod case_sensitive {
    type HashMap<'a, Node> = std::collections::HashMap<&'a str, Node, fxhash::FxBuildHasher>;
    mod shared;
    pub use shared::is_valid_keyword;
    pub use shared::KeywordProcessor;
}

#[derive(Debug, PartialEq)]
enum KeywordProcessor<'a> {
    CaseSensitive(case_sensitive::KeywordProcessor<'a>),
    CaseInsensitive(case_insensitive::KeywordProcessor<'a>),
}

macro_rules! duplicate_body {
    ($inner:expr, $var:ident, $body:expr) => {
        match $inner {
            KeywordProcessor::CaseSensitive($var) => $body,
            KeywordProcessor::CaseInsensitive($var) => $body,
        }
    };
}

#[pyclass(name = "PyKeywordProcessor")]
#[derive(PartialEq, Debug)]
pub struct PyKeywordProcessor {
    // Store owned strings
    words: Vec<String>,
    clean_names: Vec<String>,
    case_sensitive: bool,
}

#[pymethods]
impl PyKeywordProcessor {
    #[new]
    #[pyo3(signature = (case_sensitive=false))]
    fn new(case_sensitive: bool) -> Self {
        Self {
            words: Vec::new(),
            clean_names: Vec::new(),
            case_sensitive,
        }
    }

    fn __len__(&self) -> usize {
        self.words.len()
    }

    fn __repr__(&self) -> String {
        "<KeywordProcessor()>".to_string()
    }

    #[getter]
    fn case_sensitive(&self) -> bool {
        self.case_sensitive
    }

    #[pyo3(signature = (word, clean_name=None))]
    fn add_keyword(&mut self, word: String, clean_name: Option<String>) -> PyResult<()> {
        if !case_sensitive::is_valid_keyword(&word) {
            return Err(PyValueError::new_err(format!(
                "invalid keyword: {:?}",
                word
            )));
        }
        self.words.push(word.clone());
        self.clean_names.push(clean_name.unwrap_or(word));
        Ok(())
    }

    fn add_keywords_from_iter<'py>(&mut self, words: Bound<'py, PyAny>) -> PyResult<usize> {
        let mut successfull = 0;
        let mut failed_words: Vec<String> = Vec::new();
        for word in words.iter().unwrap() {
            let word: String = word.unwrap().extract::<String>().unwrap();
            let res: Result<(), PyErr> = self.add_keyword(word.clone(), None);
            if res.is_ok() {
                successfull += 1;
            } else {
                failed_words.push(word);
            }
        }
        if !failed_words.is_empty() {
            Err(PyValueError::new_err(format!(
                "invalid keywords: {:?}",
                failed_words
            )))
        } else {
            Ok(successfull)
        }
    }

    fn add_keywords_with_clean_name_from_iter<'py>(
        &mut self,
        words: Bound<'py, PyAny>,
    ) -> PyResult<()> {
        let mut successfull = 0;
        let mut failed_words: Vec<String> = Vec::new();
        for word_pair in words.iter().unwrap() {
            let (word, clean_name) = word_pair.unwrap().extract::<(String, String)>().unwrap();
            // self.add_keyword(word, Some(clean_name));
            let cloned_word = word.clone();
            let res: Result<(), PyErr> = self.add_keyword(word, Some(clean_name));
            if res.is_ok() {
                successfull += 1;
            } else {
                failed_words.push(cloned_word);
            }
        }
        if !failed_words.is_empty() {
            Err(PyValueError::new_err(format!(
                "invalid keywords: {:?}",
                failed_words
            )))
        } else {
            Ok(())
        }
    }

    fn extract_keywords(&self, text: &str) -> Vec<String> {
        let mut processor = if self.case_sensitive {
            KeywordProcessor::CaseSensitive(case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(case_insensitive::KeywordProcessor::new())
        };
        // Add keywords to the processor
        for (word, clean_name) in self.words.iter().zip(self.clean_names.iter()) {
            duplicate_body!(&mut processor, inner, {
                inner.add_keyword_with_clean_name(word, clean_name);
            });
        }
        // Extract keywords
        duplicate_body!(&processor, inner, {
            inner.extract_keywords(text).map(String::from).collect()
        })
    }

    fn extract_keywords_from_list<'py>(&self, texts: Bound<'py, PyAny>) -> Vec<Vec<String>> {
        texts
            .iter()
            .unwrap()
            .map(|py_obj| {
                let text = py_obj.unwrap().extract::<String>().unwrap();
                self.extract_keywords(&text)
            })
            .collect()
    }

    fn extract_keywords_with_span(&self, text: &str) -> Vec<(String, usize, usize)> {
        let mut processor = if self.case_sensitive {
            KeywordProcessor::CaseSensitive(case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(case_insensitive::KeywordProcessor::new())
        };
        // Add keywords to the processor
        for (word, clean_name) in self.words.iter().zip(self.clean_names.iter()) {
            duplicate_body!(&mut processor, inner, {
                inner.add_keyword_with_clean_name(word, clean_name);
            });
        }
        // Extract keywords with span
        duplicate_body!(&processor, inner, {
            if text.is_ascii() {
                inner
                    .extract_keywords_with_span(text)
                    .map(|(word, start, end)| (word.to_string(), start, end))
                    .collect()
            } else {
                let mut vec = vec![];
                let char_indices: Vec<_> = text.char_indices().collect();
                // Extract keywords with span
                for (clean_name, word_start, word_end) in inner.extract_keywords_with_span(text) {
                    // Convert byte offset to char offset for start position
                    let start_char_idx = char_indices
                        .iter()
                        .position(|(byte_idx, _)| *byte_idx == word_start)
                        .unwrap_or(0);

                    // Convert byte offset to char offset for end position
                    let end_char_idx = char_indices
                        .iter()
                        .position(|(byte_idx, _)| *byte_idx == word_end)
                        .unwrap_or_else(|| char_indices.len());

                    vec.push((clean_name.to_string(), start_char_idx, end_char_idx));
                }
                vec
            }
        })
    }

    fn extract_keywords_with_span_from_list<'py>(
        &self,
        texts: Bound<'py, PyAny>,
    ) -> Vec<Vec<(String, usize, usize)>> {
        texts
            .iter()
            .unwrap()
            .map(|py_obj| {
                let text = py_obj.unwrap().extract::<String>().unwrap();
                self.extract_keywords_with_span(&text)
            })
            .collect()
    }

    fn replace_keywords(&self, text: &str) -> String {
        let mut processor = if self.case_sensitive {
            KeywordProcessor::CaseSensitive(case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(case_insensitive::KeywordProcessor::new())
        };
        // Add keywords to the processor
        for (word, clean_name) in self.words.iter().zip(self.clean_names.iter()) {
            duplicate_body!(&mut processor, inner, {
                inner.add_keyword_with_clean_name(word, clean_name);
            });
        }
        // Replace keywords
        duplicate_body!(&processor, inner, { inner.replace_keywords(text) })
    }
}

// #[pymodule]
// fn librush(m: &Bound<'_, PyModule>) -> PyResult<()> {
//     m.add_class::<PyKeywordProcessor>()?;
//     Ok(())
// }

// TODO: benchmark `words: Vec<str>` Vs `words: PyIterator<str>` and see if there is a difference
