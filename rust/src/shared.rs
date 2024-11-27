use std::collections::hash_map::Entry;
use std::str::FromStr;
use std::sync::{Arc, RwLock};
use unicase::UniCase;
use unicode_segmentation::UnicodeSegmentation;

pub fn is_valid_keyword(word: &str) -> bool {
    if word.is_empty() {
        return false;
    }
    // Check if the word contains any non-whitespace characters
    if word.chars().all(char::is_whitespace) {
        return false;
    }
    // Check if word contains only word boundaries
    let tokens: Vec<&str> = word.split_word_bounds().collect();
    return tokens.iter().any(|&token| {
        !token
            .chars()
            .all(|c| c.is_whitespace() || c == '.' || c == ' ')
    });
}

#[derive(Default, Debug, PartialEq)]
struct UniCaseHashMap<V> {
    inner: std::collections::HashMap<UniCase<String>, V, fxhash::FxBuildHasher>,
}

impl<V> UniCaseHashMap<V> {
    pub fn entry(&mut self, k: String) -> Entry<UniCase<String>, V> {
        self.inner.entry(UniCase::unicode(k))
    }

    pub fn get(&self, k: &String) -> Option<&V> {
        self.inner.get(&UniCase::unicode(k.to_string()))
    }
}

#[derive(Debug, PartialEq)]
enum Dict<V> {
    CaseSensitive(std::collections::HashMap<String, V, fxhash::FxBuildHasher>),
    CaseInsensitive(UniCaseHashMap<V>),
}

enum NodeDictEntry<'a> {
    CaseSensitive(Entry<'a, String, Node>),
    CaseInsensitive(Entry<'a, UniCase<String>, Node>),
}

impl<'a> NodeDictEntry<'a> {
    pub fn or_default(self) -> &'a mut Node {
        match self {
            NodeDictEntry::CaseSensitive(entry) => match entry {
                Entry::Occupied(entry) => entry.into_mut(),
                Entry::Vacant(entry) => entry.insert(Node::new(true)),
            },
            NodeDictEntry::CaseInsensitive(entry) => match entry {
                Entry::Occupied(entry) => entry.into_mut(),
                Entry::Vacant(entry) => entry.insert(Node::new(false)),
            },
        }
    }
}

impl Dict<Node> {
    pub fn entry(&mut self, k: String) -> NodeDictEntry {
        match self {
            Dict::CaseSensitive(inner) => NodeDictEntry::CaseSensitive(inner.entry(k)),
            Dict::CaseInsensitive(inner) => NodeDictEntry::CaseInsensitive(inner.entry(k)),
        }
    }

    pub fn get(&self, k: &String) -> Option<&Node> {
        match self {
            Dict::CaseSensitive(inner) => inner.get(k),
            Dict::CaseInsensitive(inner) => inner.get(k),
        }
    }
}

#[derive(PartialEq, Debug)]
struct Node {
    clean_name: Option<String>,
    children: Dict<Node>,
}

impl Node {
    pub fn new(case_sensitive: bool) -> Self {
        if case_sensitive {
            Self {
                clean_name: None,
                children: Dict::CaseSensitive(Default::default()),
            }
        } else {
            Self {
                clean_name: None,
                children: Dict::CaseInsensitive(UniCaseHashMap {
                    inner: Default::default(),
                }),
            }
        }
    }
}

#[derive(Debug)]
pub struct KeywordProcessor {
    trie: Arc<RwLock<Node>>,
    len: usize,
}

impl KeywordProcessor {
    pub fn new(case_sensitive: bool) -> Self {
        Self {
            trie: Arc::new(RwLock::new(Node::new(case_sensitive))),
            len: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0 // or `self.trie.children.is_empty()`
    }

    #[inline]
    pub fn add_keyword(&mut self, word: &str) {
        self.add_keyword_with_clean_name(word, &word);
    }

    pub fn add_keyword_with_clean_name(&mut self, word: &str, clean_name: &str) {
        if !is_valid_keyword(word) {
            panic!("invalid keyword: {:?}", word);
        }

        // follwing code can cause a deadlock?
        let mut trie = &mut *self.trie.write().unwrap();

        for token in word.split_word_bounds() {
            trie = trie.children.entry(token.to_string()).or_default();
        }

        // increment `len` only if the keyword isn't already there
        if trie.clean_name.is_none() {
            self.len += 1;
        }
        // but even if there is already a keyword, the user can still overwrite its `clean_name`
        trie.clean_name = Some(clean_name.to_string());

        // locked is unlocked here
    }

    pub fn extract_keywords(
        &self,
        text: String,
        strategy: ExtractorStrategy,
    ) -> impl Iterator<Item = String> {
        let trie = self.trie.clone();
        KeywordExtractor::new(&text, trie, strategy).map(|(matched_text, _, _)| matched_text)
    }

    pub fn extract_keywords_with_span(
        &self,
        text: String,
        strategy: ExtractorStrategy,
    ) -> impl Iterator<Item = (String, usize, usize)> {
        let trie = self.trie.clone();
        KeywordExtractor::new(&text, trie, strategy)
    }

    pub fn replace_keywords(&self, text: String) -> String {
        let textref = text.to_string();
        let mut string = String::with_capacity(text.len());
        let mut prev_end = 0;
        for (keyword, start, end) in
            self.extract_keywords_with_span(textref, ExtractorStrategy::Longest)
        {
            string += &text[prev_end..start];
            string += &keyword;
            prev_end = end;
        }
        string += &text[prev_end..];
        string.shrink_to_fit();
        string
    }
}

#[derive(Default, Debug, PartialEq)]
pub enum ExtractorStrategy {
    Longest,
    #[default]
    All,
}

impl FromStr for ExtractorStrategy {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "longest" => Ok(ExtractorStrategy::Longest),
            "all" => Ok(ExtractorStrategy::All),
            _ => Err(()),
        }
    }
}

struct KeywordExtractor {
    idx: usize,
    tokens: Vec<(usize, String)>,
    trie: Arc<RwLock<Node>>,
    matches: Vec<(String, usize, usize)>, // Store all matches found
    strategy: ExtractorStrategy,
}

impl KeywordExtractor {
    fn new(text: &String, trie: Arc<RwLock<Node>>, strategy: ExtractorStrategy) -> Self {
        Self {
            idx: 0,
            tokens: text
                .split_word_bound_indices()
                .into_iter()
                .map(|(i, s)| (i, s.to_string()))
                .collect(),
            trie: trie,
            matches: Vec::new(),
            strategy: strategy,
        }
    }

    fn find_matches_at_position(&mut self, start_idx: usize) {
        let mut node = &*self.trie.read().unwrap();
        let mut current_idx = start_idx;

        while current_idx < self.tokens.len() {
            let (token_start_idx, token) = &self.tokens[current_idx];

            if let Some(child) = node.children.get(token) {
                node = child;
                if let Some(clean_name) = &node.clean_name {
                    // Found a match, store it with the clean_name
                    let start_pos = self.tokens[start_idx].0;
                    let end_pos = token_start_idx + token.len();
                    self.matches
                        .push((clean_name.to_string(), start_pos, end_pos));
                }
                current_idx += 1;
            } else {
                break;
            }
        }
    }

    fn find_longest_match(&mut self, start_idx: usize) -> usize {
        let mut node = &*self.trie.read().unwrap();
        let mut current_idx = start_idx;
        let mut longest_match = None;
        let mut end_idx = start_idx;

        while current_idx < self.tokens.len() {
            let (token_start_idx, token) = &self.tokens[current_idx];

            if let Some(child) = node.children.get(token) {
                node = child;
                if let Some(clean_name) = &node.clean_name {
                    // Found a match, store it with the clean_name
                    let start_pos = self.tokens[start_idx].0;
                    let end_pos = token_start_idx + token.len();
                    longest_match = Some((clean_name.to_string(), start_pos, end_pos));
                    end_idx = current_idx;
                }
                current_idx += 1;
            } else {
                break;
            }
        }

        if let Some(matched) = longest_match {
            self.matches.push(matched);
        }

        end_idx
    }
}

impl Iterator for KeywordExtractor {
    type Item = (String, usize, usize);

    fn next(&mut self) -> Option<Self::Item> {
        if self.strategy == ExtractorStrategy::Longest {
            let mut end_idx = self.find_longest_match(self.idx);
            while end_idx == self.idx {
                if self.idx >= self.tokens.len() {
                    break;
                }
                self.idx += 1; // skip the current token since there is no match
                end_idx = self.find_longest_match(self.idx);
            }
            self.idx = end_idx + 1;
            if !self.matches.is_empty() {
                Some(self.matches.remove(0))
            } else {
                None
            }
        } else {
            // this is not a real iterator
            while self.idx < self.tokens.len() {
                // this will only performed once per iterator
                self.find_matches_at_position(self.idx);
                self.idx += 1;
            }
            if !self.matches.is_empty() {
                Some(self.matches.remove(0))
            } else {
                None
            }
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, Some(self.tokens.len()))
    }
}
