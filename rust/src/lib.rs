mod base;

#[cfg(not(test))]
use pyo3::prelude::*;

#[derive(Debug, PartialEq)]
enum KeywordProcessor<'a> {
    CaseSensitive(base::case_sensitive::KeywordProcessor<'a>),
    CaseInsensitive(base::case_insensitive::KeywordProcessor<'a>),
}

macro_rules! duplicate_body {
    ($inner:expr, $var:ident, $body:expr) => {
        match $inner {
            KeywordProcessor::CaseSensitive($var) => $body,
            KeywordProcessor::CaseInsensitive($var) => $body,
        }
    };
}

#[cfg(not(test))]
#[pyclass(name = "PyKeywordProcessor")]
#[derive(PartialEq, Debug)]
struct PyKeywordProcessor {
    // Store owned strings
    words: Vec<String>,
    clean_words: Vec<String>,
    case_sensitive: bool,
}

#[cfg(not(test))]
#[pymethods]
impl PyKeywordProcessor {
    #[new]
    fn new(case_sensitive: bool) -> Self {
        Self {
            words: Vec::new(),
            clean_words: Vec::new(),
            case_sensitive,
        }
    }

    fn __len__(&self) -> usize {
        self.words.len()
    }

    fn __repr__(&self) -> String {
        "< KeywordProcessor() >".to_string()
    }

    #[getter]
    fn case_sensitive(&self) -> bool {
        self.case_sensitive
    }

    #[pyo3(signature = (word, clean_word=None))]
    fn add_keyword(&mut self, word: String, clean_word: Option<String>) {
        self.words.push(word.clone());
        self.clean_words.push(clean_word.unwrap_or(word));
    }

    fn add_keywords_from_iter<'py>(&mut self, words: Bound<'py, PyAny>) {
        for word in words.iter().unwrap() {
            let word = word.unwrap().extract::<String>().unwrap();
            self.add_keyword(word, None);
        }
    }

    fn add_keywords_with_clean_word_from_iter<'py>(&mut self, words: Bound<'py, PyAny>) {
        for word_pair in words.iter().unwrap() {
            let (word, clean_word) = word_pair.unwrap().extract::<(String, String)>().unwrap();
            self.add_keyword(word, Some(clean_word));
        }
    }

    fn extract_keywords(&self, text: &str) -> Vec<String> {
        let mut processor = if self.case_sensitive {
            KeywordProcessor::CaseSensitive(base::case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(base::case_insensitive::KeywordProcessor::new())
        };

        // Add keywords to the processor
        for (word, clean_word) in self.words.iter().zip(self.clean_words.iter()) {
            duplicate_body!(&mut processor, inner, {
                inner.add_keyword_with_clean_word(word, clean_word);
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
            KeywordProcessor::CaseSensitive(base::case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(base::case_insensitive::KeywordProcessor::new())
        };

        // Add keywords to the processor
        for (word, clean_word) in self.words.iter().zip(self.clean_words.iter()) {
            duplicate_body!(&mut processor, inner, {
                inner.add_keyword_with_clean_word(word, clean_word);
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
                let mut it = text.char_indices().enumerate();
                for (clean_word, mut word_start, mut word_end) in
                    inner.extract_keywords_with_span(text)
                {
                    for (idx, (char_idx, _)) in it.by_ref() {
                        if char_idx == word_start {
                            word_start = idx;
                            break;
                        }
                    }
                    {
                        let old_word_end = word_end;
                        let mut last_idx = 0;
                        for (idx, (char_idx, _)) in it.by_ref() {
                            last_idx = idx;
                            if word_end == char_idx {
                                word_end = idx;
                                break;
                            }
                        }
                        if word_end == old_word_end {
                            word_end = last_idx + 1;
                        }
                    }
                    vec.push((clean_word.to_string(), word_start, word_end));
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
            KeywordProcessor::CaseSensitive(base::case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(base::case_insensitive::KeywordProcessor::new())
        };

        // Add keywords to the processor
        for (word, clean_word) in self.words.iter().zip(self.clean_words.iter()) {
            duplicate_body!(&mut processor, inner, {
                inner.add_keyword_with_clean_word(word, clean_word);
            });
        }

        // Replace keywords
        duplicate_body!(&processor, inner, { inner.replace_keywords(text) })
    }
}

#[cfg(not(test))]
#[pymodule]
fn librush(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyKeywordProcessor>()?;
    Ok(())
}

// TODO: benchmark `words: Vec<str>` Vs `words: PyIterator<str>` and see if there is a difference
