import codecs
from utils import read_in_corpus

lines = read_in_corpus('./data/german-dict-2.txt')
output_words = []
for line in lines:
    words = line.split(' ')[0]
    maybe_more_words = words.split(',')
    for word in maybe_more_words:
        output_words.append(word.lower())

f = codecs.open("data/german-dict-final.txt", "w+",  "utf-8")
f.write('\n'.join(output_words))
