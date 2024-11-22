use unicode_segmentation::UnicodeSegmentation;

#[derive(Default, PartialEq, Debug)]
struct Node<'a> {
    clean_word: Option<&'a str>, // TODO: make this an enum that can hold a reference
    children: super::HashMap<'a, Node<'a>>,
}

#[derive(Default, PartialEq, Debug)]
pub struct KeywordProcessor<'a> {
    trie: Node<'a>,
    len: usize, // the number of keywords the struct contains (not the number of nodes)
}

impl<'a> KeywordProcessor<'a> {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        // or `self.trie.children.is_empty()`
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
        println!("{:?}", tokens);
        return tokens.iter().any(|&token| {
            !token
                .chars()
                .all(|c| c.is_whitespace() || c == '.' || c == ' ')
        });
    }

    #[inline]
    pub fn add_keyword_with_clean_word(
        &mut self,
        word: &'a str,
        clean_word: &'a str, // make this call an `_impl...()` method that takes an option
    ) {
        if !Self::is_valid_keyword(word) {
            return;
        }

        let mut trie = &mut self.trie;

        for token in word.split_word_bounds() {
            trie = trie.children.entry(token).or_default();
        }

        // increment `len` only if the keyword isn't already there
        if trie.clean_word.is_none() {
            self.len += 1;
        }
        // but even if there is already a keyword, the user can still overwrite its `clean_word`
        trie.clean_word = Some(clean_word.as_ref());
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
    idx: usize,
    tokens: Vec<(usize, &'a str)>,
    trie: &'a Node<'a>,
    text: &'a str,
    matches: Vec<(&'a str, usize, usize)>, // Store all matches found
}

impl<'a> KeywordExtractor<'a> {
    fn new(text: &'a str, trie: &'a Node) -> Self {
        Self {
            idx: 0,
            tokens: text.split_word_bound_indices().collect(),
            trie,
            text,
            matches: Vec::new(),
        }
    }

    fn find_matches_at_position(&mut self, start_idx: usize) {
        let mut node = self.trie;
        let mut current_idx = start_idx;

        while current_idx < self.tokens.len() {
            let (token_start_idx, token) = self.tokens[current_idx];

            if let Some(child) = node.children.get(token) {
                node = child;
                if let Some(clean_word) = node.clean_word {
                    // Found a match, store it with the clean_word
                    let start_pos = self.tokens[start_idx].0;
                    let end_pos = token_start_idx + token.len();
                    self.matches.push((clean_word, start_pos, end_pos));
                }
                current_idx += 1;
            } else {
                break;
            }
        }
    }
}

impl<'a> Iterator for KeywordExtractor<'a> {
    type Item = (&'a str, usize, usize);

    fn next(&mut self) -> Option<Self::Item> {
        while self.idx < self.tokens.len() {
            self.find_matches_at_position(self.idx);
            self.idx += 1;
        }

        if !self.matches.is_empty() {
            Some(self.matches.remove(0))
        } else {
            None
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (0, Some(self.tokens.len()))
    }
}
