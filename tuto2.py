from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_text = "this is an example showing off stop work filtration"
stop_words = set(stopwords.words('english'))

words = word_tokenize(example_text)

filtered_words = list(filter(lambda x: x not in stop_words, words))

print(filtered_words)
