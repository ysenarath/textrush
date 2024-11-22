use unicode_segmentation::UnicodeSegmentation;

#[derive(Default, PartialEq, Debug)]
struct Node<'a> {
    clean_word: Option<&'a str>,
    children: super::HashMap<'a, Node<'a>>,
}

#[derive(Default, PartialEq, Debug)]
pub struct KeywordProcessor<'a> {
    trie: Node<'a>,
    len: usize,
}

impl<'a> KeywordProcessor<'a> {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    #[inline]
    pub fn add_keyword(&mut self, word: &'a str) {
        self.add_keyword_with_clean_word(word, word);
    }

    fn is_valid_keyword(word: &str) -> bool {
        if word.is_empty() {
            return false;
        }
        // Check if the word contains any non-whitespace characters
        if word.chars().all(char::is_whitespace) {
            return false;
        }
        // Check if word contains only word boundaries
        let tokens: Vec<&str> = word.split_word_bounds().collect();
        tokens.iter().any(|&token| {
            !token
                .chars()
                .all(|c| c.is_whitespace() || c == '.' || c == ' ')
        })
    }

    #[inline]
    pub fn add_keyword_with_clean_word(&mut self, word: &'a str, clean_word: &'a str) {
        // Skip invalid keywords
        if !Self::is_valid_keyword(word) {
            return;
        }

        let mut trie = &mut self.trie;
        let tokens: Vec<&str> = word.split_word_bounds().collect();

        // Only add if we have valid tokens
        if !tokens.is_empty() {
            for token in tokens {
                trie = trie.children.entry(token).or_default();
            }

            // increment `len` only if the keyword isn't already there
            if trie.clean_word.is_none() {
                self.len += 1;
            }
            trie.clean_word = Some(clean_word.as_ref());
        }
    }

    pub fn add_keywords_from_iter(&mut self, iter: impl IntoIterator<Item = &'a str>) {
        for word in iter {
            self.add_keyword(word.as_ref());
        }
    }

    pub fn add_keywords_with_clean_word_from_iter<I>(&mut self, iter: I)
    where
        I: IntoIterator<Item = (&'a str, &'a str)>,
    {
        for (word, clean_word) in iter {
            self.add_keyword_with_clean_word(word.as_ref(), clean_word.as_ref());
        }
    }

    pub fn extract_keywords(&'a self, text: &'a str) -> impl Iterator<Item = &'a str> + 'a {
        KeywordExtractor::new(text, &self.trie).map(|(matched_text, _, _)| matched_text)
    }

    pub fn extract_keywords_with_span(
        &'a self,
        text: &'a str,
    ) -> impl Iterator<Item = (&'a str, usize, usize)> + 'a {
        KeywordExtractor::new(text, &self.trie)
    }

    pub fn replace_keywords(&self, text: &str) -> String {
        let mut string = String::with_capacity(text.len());
        let mut prev_end = 0;
        for (keyword, start, end) in self.extract_keywords_with_span(text) {
            string += &text[prev_end..start];
            string += &keyword;
            prev_end = end;
        }
        string += &text[prev_end..];
        string.shrink_to_fit();
        string
    }
}

struct KeywordExtractor<'a> {
    text: &'a str,
    tokens: Vec<(usize, &'a str)>,
    trie: &'a Node<'a>,
    current_pos: usize,
    processed_until: usize,
}

impl<'a> KeywordExtractor<'a> {
    fn new(text: &'a str, trie: &'a Node) -> Self {
        Self {
            text,
            tokens: text.split_word_bound_indices().collect(),
            trie,
            current_pos: 0,
            processed_until: 0,
        }
    }

    fn find_longest_match(&self, start_pos: usize) -> Option<(&'a str, usize, usize)> {
        let mut node = self.trie;
        let mut current_idx = start_pos;
        let mut last_match = None;

        while current_idx < self.tokens.len() {
            let (token_start_idx, token) = self.tokens[current_idx];

            if let Some(child) = node.children.get(token) {
                node = child;

                if let Some(clean_word) = node.clean_word {
                    let match_start = self.tokens[start_pos].0;
                    let match_end = token_start_idx + token.len();

                    // Validate indices
                    if match_start < match_end && match_end <= self.text.len() {
                        last_match = Some((clean_word, match_start, match_end));
                    }
                }
                current_idx += 1;
            } else {
                break;
            }
        }

        last_match
    }
}

impl<'a> Iterator for KeywordExtractor<'a> {
    type Item = (&'a str, usize, usize);

    fn next(&mut self) -> Option<Self::Item> {
        while self.current_pos < self.tokens.len() {
            // Skip positions we've already processed
            if self.current_pos < self.processed_until {
                self.current_pos += 1;
                continue;
            }

            if let Some(match_info) = self.find_longest_match(self.current_pos) {
                let (clean_word, start, end) = match_info;
                // Update processed_until to avoid overlapping matches
                self.processed_until = self
                    .tokens
                    .iter()
                    .position(|&(pos, _)| pos >= end)
                    .unwrap_or(self.tokens.len());
                self.current_pos += 1;
                return Some((clean_word, start, end));
            }

            self.current_pos += 1;
        }

        None
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, Some(self.tokens.len()))
    }
}
