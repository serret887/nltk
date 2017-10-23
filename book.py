import nltk
from CorrectWords import correct_text_generic
from pprint import pprint
import re
import string
import logging
from nltk.corpus import wordnet
import enchant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
engDict = enchant.Dict("en_US")


def tokenize_text(text):
    sentences = nltk.sent_tokenize(text)
    word_tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
    return word_tokens


corpus = ["FINALY teh A brown fox wasn't that quick and he couldn't win the race",
"Hey that's a great deal! I just bought a phoneeeeeeeee for $199",
"@@You'll (learn) a **lot** in the book. Python is an amazing language !@@"]

def remove_repeated_characters(tokens):
    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'
    #pprint(tokens)
    def replace(new_word, old_word):
        #if wordnet.synsets(old_word):
        if new_word == old_word or engDict.check(new_word):
            return new_word
        old_word = new_word
        new_word = repeat_pattern.sub(match_substitution, new_word)
        logger.info("Replacing Duplicate Characters\
                    %s with new %s",old_word, new_word)
        return replace(new_word, old_word)

    correct_tokens = [replace(word, None) for word in tokens]
    return correct_tokens

def remove_characters_before_tokenization(sentence, keep_apostrophes=False):
    sentence = sentence.strip()
    if keep_apostrophes:
        PATTERN = r'[?|$|&|*|%|@|(|)|~]' # add other characters here to remove them
        filtered_sentence = re.sub(PATTERN, r'', sentence)
    else:
        PATTERN = r'[^a-zA-Z0-9 ]' # only extract alpha-numeric characters
        filtered_sentence = re.sub(PATTERN, r'', sentence)
    return filtered_sentence


def remove_characters_after_tokenization(tokens):
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub('', token) for token in tokens])
    return filtered_tokens

def expand_contractions(sentence, contraction_mapping):
    contractions_pattern = re.compile('({})'.format('|'\
                                    .join(contraction_mapping.keys())),
                                        flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())
        first_expanded_contraction = expanded_contraction.split(';')[0]
        expanded_contraction = first_expanded_contraction
        logger.info("Expanding Contractions match: %s -> changed: %s", match, expanded_contraction)
        return expanded_contraction

    expanded_sentence = contractions_pattern.sub(expand_match,sentence)
    return expanded_sentence


def remove_stop_words(tokens):

    stopword_list = nltk.corpus.stopwords.words('english')

    filtered_tokens = [token for token in tokens
                        if token not in stopword_list]
    return filtered_tokens


from contractions import *

cleanedText = [remove_characters_before_tokenization(text, True)
                for text in corpus]

expanded_corpus = [expand_contractions(sentence, CONTRACTION_MAP)
                    for sentence in cleanedText]


tokenizeText = [tokenize_text(text) for text in expanded_corpus]

removed_stop_words = [[remove_stop_words(tokens)
                        for tokens in sentence_tokens]
                        for sentence_tokens in tokenizeText]


removed_not_good_words = [[remove_repeated_characters(text)
                            for text in sentence_tokens]
                            for sentence_tokens in removed_stop_words]

pprint(removed_not_good_words)

corrected_text = [[[correct_text_generic(word)
                            for word in text]
                            for text in sentence_tokens]
                            for sentence_tokens in removed_not_good_words]

pprint(corrected_text)
#pprint(tokenizeText)
# when removing stop words I am removing also (not | no ) this words are
# essentials to sentiment analisis
