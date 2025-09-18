# text_analyzer.py
import nltk
import re
import os

# Ensure required NLTK resources are available
for resource in ['punkt_tab', 'stopwords']:
    try:
        if resource == 'punkt_tab':
            nltk.data.find('tokenizers/punkt_tab')
        else:
            nltk.data.find(f'corpora/{resource}')
    except LookupError:
        print(f"📥 Downloading NLTK resource: {resource}")
        nltk.download(resource)

# Global cache for stopwords and sentiment dictionaries
STOP_WORDS = None
POSITIVE_WORDS = None
NEGATIVE_WORDS = None

def load_stop_words():
    """Load all stopwords from resources/StopWords directory into a set."""
    stop_words = set()
    stopwords_dir = "resources/StopWords"
    for filename in os.listdir(stopwords_dir):
        filepath = os.path.join(stopwords_dir, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                words = [w.strip().lower() for w in line.split("|") if w.strip()]
                stop_words.update(words)
    return stop_words

def load_sentiment_words(stop_words):
    """Load positive and negative words, excluding stopwords and comments."""
    positive_words = set()
    negative_words = set()

    with open("resources/MasterDictionary/positive-words.txt", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip().lower()
            if word and not word.startswith(";") and word not in stop_words:
                positive_words.add(word)

    with open("resources/MasterDictionary/negative-words.txt", "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip().lower()
            if word and not word.startswith(";") and word not in stop_words:
                negative_words.add(word)

    return positive_words, negative_words

def count_syllables(word):
    """Count syllables in a word using a simple heuristic."""
    word = word.lower()
    if len(word) > 2 and word.endswith("e"):
        word = word[:-1]
    if len(word) > 3 and (word.endswith("es") or word.endswith("ed")):
        word = word[:-2]

    vowels = "aeiouy"
    count = 0
    prev_is_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel

    return max(1, count)

def count_personal_pronouns(text):
    """Count personal pronouns (I, we, my, ours, us) excluding country name 'US'."""
    pattern = r"\b(I|we|my|ours|us)\b"
    matches = re.findall(pattern, text, re.IGNORECASE)
    # Exclude 'US' when it's likely the country (standalone and capitalized)
    count = 0
    for pronoun in matches:
        if pronoun.lower() == 'us':
            if not re.search(r'\bUS\b', text):
                count += 1
        else:
            count += 1
    return count

def analyze_text(text):
    """Perform text analysis and return dictionary of computed metrics."""

    global STOP_WORDS, POSITIVE_WORDS, NEGATIVE_WORDS
    if STOP_WORDS is None:
        STOP_WORDS = load_stop_words()
        POSITIVE_WORDS, NEGATIVE_WORDS = load_sentiment_words(STOP_WORDS)

    # Tokenization
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)

    # Clean words: only alphabetic, lowercase, no stopwords
    cleaned_words = [w.lower() for w in words if w.isalpha() and w.lower() not in STOP_WORDS]

    # Sentiment
    positive_score = sum(1 for w in cleaned_words if w in POSITIVE_WORDS)
    negative_score = sum(1 for w in cleaned_words if w in NEGATIVE_WORDS)

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 1e-6)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 1e-6)

    # Readability
    avg_sentence_length = len(cleaned_words) / len(sentences) if sentences else 0
    complex_words = [w for w in cleaned_words if count_syllables(w) > 2]
    percentage_complex_words = (len(complex_words) / len(cleaned_words)) if cleaned_words else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Other metrics
    avg_words_per_sentence = avg_sentence_length
    complex_word_count = len(complex_words)
    word_count = len(cleaned_words)

    total_syllables = sum(count_syllables(w) for w in cleaned_words)
    syllable_per_word = (total_syllables / word_count) if word_count else 0

    personal_pronouns = count_personal_pronouns(text)

    total_chars = sum(len(w) for w in cleaned_words)
    avg_word_length = (total_chars / word_count) if word_count else 0

    return {
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": round(polarity_score, 4),
        "SUBJECTIVITY SCORE": round(subjectivity_score, 4),
        "AVG SENTENCE LENGTH": round(avg_sentence_length, 2),
        "PERCENTAGE OF COMPLEX WORDS": round(percentage_complex_words * 100, 2),
        "FOG INDEX": round(fog_index, 2),
        "AVG NUMBER OF WORDS PER SENTENCE": round(avg_words_per_sentence, 2),
        "COMPLEX WORD COUNT": complex_word_count,
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": round(syllable_per_word, 2),
        "PERSONAL PRONOUNS": personal_pronouns,
        "AVG WORD LENGTH": round(avg_word_length, 2),
    }