from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

ps = PorterStemmer()
#example_words = ['pythonic', 'pythonistic','pythoner','pythoning' ]
example_words = word_tokenize( " is very important to learn python because pythoning is teh best for a young pythoner ")
stem = [ps.stem(w) for w in example_words]

print(stem)
