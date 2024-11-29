use std::collections::hash_map::{Entry, Keys};
use std::iter::Map;
use std::str::FromStr;
use unicase::UniCase;
use unicode_segmentation::UnicodeSegmentation;

pub fn is_valid_keyword(word: &str) -> bool {
    // check if the word is empty
    // - non empty words can still be invalid
    // - e.g. " " or "." is not a valid keyword
    if word.is_empty() {
        return false;
    }
    // Check if number of words is greater than 1
    let tokens: Vec<&str> = word.split_word_bounds().collect();
    if tokens.len() == 0 {
        return false;
    }
    tokens
        .iter()
        .any(|t| !t.chars().all(|c| c.is_whitespace() || c == '.' || c == ' '))
}

#[derive(Default, Debug, PartialEq)]
struct UniCaseHashMap<V> {
    inner: std::collections::HashMap<UniCase<String>, V, fxhash::FxBuildHasher>,
}

impl<V> UniCaseHashMap<V> {
    pub fn entry(&mut self, k: String) -> Entry<UniCase<String>, V> {
        self.inner.entry(UniCase::unicode(k))
    }

    pub fn get(&self, k: &str) -> Option<&V> {
        self.inner.get(&UniCase::unicode(k.to_string()))
    }

    pub fn keys(&self) -> Keys<UniCase<String>, V> {
        self.inner.keys()
    }
}

#[derive(Debug, PartialEq)]
enum HashMap<V> {
    CaseSensitive(std::collections::HashMap<String, V, fxhash::FxBuildHasher>),
    CaseInsensitive(UniCaseHashMap<V>),
}

enum HashMapEntry<'a, V> {
    CaseSensitive(Entry<'a, String, V>),
    CaseInsensitive(Entry<'a, UniCase<String>, V>),
}

impl<'a> HashMapEntry<'a, Node> {
    pub fn or_default(self) -> &'a mut Node {
        match self {
            HashMapEntry::CaseSensitive(entry) => match entry {
                Entry::Occupied(entry) => entry.into_mut(),
                Entry::Vacant(entry) => entry.insert(Node::new(true)),
            },
            HashMapEntry::CaseInsensitive(entry) => match entry {
                Entry::Occupied(entry) => entry.into_mut(),
                Entry::Vacant(entry) => entry.insert(Node::new(false)),
            },
        }
    }
}

enum HashMapKeys<'a> {
    CaseSensitive(Map<Keys<'a, String, Node>, fn(&String) -> &str>),
    CaseInsensitive(Map<Keys<'a, UniCase<String>, Node>, fn(&UniCase<String>) -> &str>),
}

impl<'a> Iterator for HashMapKeys<'a> {
    type Item = &'a str;

    fn next(&mut self) -> Option<Self::Item> {
        match self {
            HashMapKeys::CaseSensitive(inner) => inner.next(),
            HashMapKeys::CaseInsensitive(inner) => inner.next(),
        }
    }
}

impl HashMap<Node> {
    pub fn entry(&mut self, k: String) -> HashMapEntry<Node> {
        match self {
            HashMap::CaseSensitive(inner) => HashMapEntry::CaseSensitive(inner.entry(k)),
            HashMap::CaseInsensitive(inner) => HashMapEntry::CaseInsensitive(inner.entry(k)),
        }
    }

    pub fn get(&self, k: &str) -> Option<&Node> {
        match self {
            HashMap::CaseSensitive(inner) => inner.get(k),
            HashMap::CaseInsensitive(inner) => inner.get(k),
        }
    }

    pub fn keys(&self) -> HashMapKeys {
        match self {
            HashMap::CaseSensitive(inner) => {
                HashMapKeys::CaseSensitive(inner.keys().map(|k| k.as_str()))
            }
            HashMap::CaseInsensitive(inner) => {
                HashMapKeys::CaseInsensitive(inner.keys().map(|k| k.as_str()))
            }
        }
    }
}

#[derive(PartialEq, Debug)]
pub struct Node {
    clean_name: Option<String>,
    children: HashMap<Node>,
}

impl Node {
    pub fn new(case_sensitive: bool) -> Self {
        if case_sensitive {
            Self {
                clean_name: None,
                children: HashMap::CaseSensitive(Default::default()),
            }
        } else {
            Self {
                clean_name: None,
                children: HashMap::CaseInsensitive(UniCaseHashMap {
                    inner: Default::default(),
                }),
            }
        }
    }
}

#[derive(Debug)]
pub struct KeywordProcessor {
    trie: Node,
    len: usize,
}

impl KeywordProcessor {
    pub fn new(case_sensitive: bool) -> Self {
        Self {
            trie: Node::new(case_sensitive),
            len: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0 // or `self.trie.children.is_empty()`
    }

    pub fn add_keyword_with_clean_name(&mut self, word: &str, clean_name: &str) {
        if !is_valid_keyword(word) {
            panic!("invalid keyword: {:?}", word);
        }
        // follwing code can cause a deadlock?
        let mut trie = &mut self.trie;
        // locked is unlocked here
        for token in word.split_word_bounds() {
            // let temp = trie.children.get(&token.to_string()).unwrap();
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

    #[inline]
    pub fn add_keyword(&mut self, word: &str) {
        self.add_keyword_with_clean_name(word, &word);
    }

    pub fn remove_keyword(&mut self, word: &str) {
        if !is_valid_keyword(word) {
            panic!("invalid keyword: {:?}", word);
        }
        // follwing code can cause a deadlock?
        let mut trie = &mut self.trie;
        // locked is unlocked here
        for token in word.split_word_bounds() {
            // if none return, or get the node - do not create an entry
            // trie must be mutable
            trie = match trie.children.entry(token.to_string()) {
                HashMapEntry::CaseSensitive(entry) => match entry {
                    Entry::Occupied(entry) => entry.into_mut(),
                    Entry::Vacant(_) => return,
                },
                HashMapEntry::CaseInsensitive(entry) => match entry {
                    Entry::Occupied(entry) => entry.into_mut(),
                    Entry::Vacant(_) => return,
                },
            };
        }
        // remove clean_name
        if trie.clean_name.is_some() {
            trie.clean_name = None;
            self.len -= 1;
        }
    }

    pub fn get_all_keywords_with_clean_names(&self) -> AllKeywordsIterator {
        // should return an iterator over all keywords, not clean_names
        AllKeywordsIterator::new(&self.trie)
    }

    pub fn extract_keywords(
        &self,
        text: String,
        strategy: ExtractorStrategy,
    ) -> Map<KeywordExtractor, fn((String, usize, usize)) -> String> {
        KeywordExtractor::new(&text, &self.trie, strategy).map(|(matched_text, _, _)| matched_text)
    }

    pub fn extract_keywords_with_span(
        &self,
        text: String,
        strategy: ExtractorStrategy,
    ) -> KeywordExtractor {
        KeywordExtractor::new(&text, &self.trie, strategy)
    }

    pub fn replace_keywords(&self, text: String) -> String {
        let textref = text.to_string();
        // Create a new empty String with at least the specified capacity
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

pub struct KeywordExtractor<'t> {
    idx: usize,
    tokens: Vec<(usize, String)>,
    trie: &'t Node,
    matches: Vec<(String, usize, usize)>, // Store all matches found
    strategy: ExtractorStrategy,
}

impl<'t> KeywordExtractor<'t> {
    fn new(text: &String, trie: &'t Node, strategy: ExtractorStrategy) -> Self {
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
        let mut node = self.trie;
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
        let mut node = self.trie;
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

impl<'t> Iterator for KeywordExtractor<'t> {
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

pub struct AllKeywordsIterator<'t> {
    stack: Vec<(String, &'t Node)>,
}

impl<'t> AllKeywordsIterator<'t> {
    pub fn new(root: &'t Node) -> Self {
        let stack = vec![("".to_string(), root)];
        Self { stack }
    }
}

impl<'t> Iterator for AllKeywordsIterator<'t> {
    type Item = (String, &'t str);

    fn next(&mut self) -> Option<Self::Item> {
        while let Some((prefix, node)) = self.stack.pop() {
            for token in node.children.keys() {
                let value = node.children.get(token).unwrap();
                self.stack.push((format!("{}{}", prefix, token), value));
            }
            if let Some(clean_name) = &node.clean_name {
                return Some((prefix, clean_name.as_str()));
            }
        }
        None
    }
}
