mod base;

#[cfg(not(test))]
use pyo3::prelude::*;

#[allow(dead_code)]
#[derive(Debug, PartialEq)]
enum KeywordProcessor<'a> {
    CaseSensitive(base::case_sensitive::KeywordProcessor<'a>),
    CaseInsensitive(base::case_insensitive::KeywordProcessor<'a>),
}

#[allow(unused_macros)]
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
    clean_names: Vec<String>,
    case_sensitive: bool,
}

#[cfg(not(test))]
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
        "< KeywordProcessor() >".to_string()
    }

    #[getter]
    fn case_sensitive(&self) -> bool {
        self.case_sensitive
    }

    #[pyo3(signature = (word, clean_name=None))]
    fn add_keyword(&mut self, word: String, clean_name: Option<String>) {
        self.words.push(word.clone());
        self.clean_names.push(clean_name.unwrap_or(word));
    }

    fn add_keywords_from_iter<'py>(&mut self, words: Bound<'py, PyAny>) {
        for word in words.iter().unwrap() {
            let word = word.unwrap().extract::<String>().unwrap();
            self.add_keyword(word, None);
        }
    }

    fn add_keywords_with_clean_name_from_iter<'py>(&mut self, words: Bound<'py, PyAny>) {
        for word_pair in words.iter().unwrap() {
            let (word, clean_name) = word_pair.unwrap().extract::<(String, String)>().unwrap();
            self.add_keyword(word, Some(clean_name));
        }
    }

    fn extract_keywords(&self, text: &str) -> Vec<String> {
        let mut processor = if self.case_sensitive {
            KeywordProcessor::CaseSensitive(base::case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(base::case_insensitive::KeywordProcessor::new())
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
            KeywordProcessor::CaseSensitive(base::case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(base::case_insensitive::KeywordProcessor::new())
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
            KeywordProcessor::CaseSensitive(base::case_sensitive::KeywordProcessor::new())
        } else {
            KeywordProcessor::CaseInsensitive(base::case_insensitive::KeywordProcessor::new())
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

#[cfg(not(test))]
#[pymodule]
fn librush(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyKeywordProcessor>()?;
    Ok(())
}

// TODO: benchmark `words: Vec<str>` Vs `words: PyIterator<str>` and see if there is a difference
