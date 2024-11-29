use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
#[path = "./versions/lib_v0_0_2.rs"]
mod lib_v0_0_2;
mod shared;
use std::str::FromStr;

#[pyclass(name = "PyKeywordProcessor")]
#[derive(Debug)]
struct PyKeywordProcessor {
    processor: shared::KeywordProcessor,
}

#[pymethods]
impl PyKeywordProcessor {
    #[new]
    #[pyo3(signature = (case_sensitive=false))]
    fn new(case_sensitive: bool) -> Self {
        Self {
            processor: shared::KeywordProcessor::new(case_sensitive),
        }
    }

    fn __len__(&self) -> usize {
        self.processor.len()
    }

    fn __repr__(&self) -> String {
        "<KeywordProcessor()>".to_string()
    }

    #[pyo3(signature = (word, clean_name=None))]
    fn add_keyword(&mut self, word: String, clean_name: Option<String>) -> PyResult<()> {
        if !shared::is_valid_keyword(&word) {
            return Err(PyValueError::new_err(format!(
                "invalid keyword: {:?}",
                word
            )));
        }
        if let Some(f) = clean_name {
            self.processor.add_keyword_with_clean_name(&word, &f);
        } else {
            self.processor.add_keyword(&word);
        }
        Ok(())
    }

    fn remove_keyword(&mut self, word: &str) {
        self.processor.remove_keyword(word);
    }

    #[pyo3(signature = (text, strategy="all"))]
    fn extract_keywords(&self, text: String, strategy: &str) -> Vec<String> {
        let strategy = shared::ExtractorStrategy::from_str(strategy).unwrap();
        self.processor
            .extract_keywords(text, strategy)
            .map(String::from)
            .collect()
    }

    #[pyo3(signature = (text, strategy="all"))]
    fn extract_keywords_with_span(
        &self,
        text: String,
        strategy: &str,
    ) -> Vec<(String, usize, usize)> {
        let strategy = shared::ExtractorStrategy::from_str(strategy).unwrap();
        let inner = &self.processor;
        // Extract keywords with span
        if text.is_ascii() {
            inner.extract_keywords_with_span(text, strategy).collect()
        } else {
            let mut vec = vec![];
            let char_indices: Vec<_> = text.char_indices().collect();
            // Extract keywords with span
            for (clean_name, word_start, word_end) in
                inner.extract_keywords_with_span(text, strategy)
            {
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
    }

    fn get_all_keywords(&self) -> Vec<(String, &str)> {
        self.processor.get_all_keywords().collect()
    }

    fn replace_keywords(&self, text: String) -> String {
        self.processor.replace_keywords(text)
    }

    fn is_empty(&self) -> bool {
        self.processor.is_empty()
    }
}

#[pymodule]
fn librush(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyKeywordProcessor>()?;
    register_submodule(m)?;
    Ok(())
}

fn register_submodule(m: &Bound<'_, PyModule>) -> PyResult<()> {
    let v1 = PyModule::new_bound(m.py(), "v0_0_2")?;
    v1.add_class::<lib_v0_0_2::PyKeywordProcessor>()?;
    m.add_submodule(&v1)?;
    Ok(())
}
