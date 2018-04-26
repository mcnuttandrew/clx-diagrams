import re
from utils import read_in_corpus

lines = read_in_corpus('./data/english-cmudict.dx1.txt')
output_words = []
# splitter = re.search('^(\w*)(\S+|\()')
for line in lines:
    # .split(s)
    # print line
    # words = splitter.findall(line)

    # print re.search('(^|\{)(\w*)(\S|\()', line).group(0)
    # word = words[0]
    word = re.search('(\w*)(|\S|[\P{P}-])', line).group(0)
    # print word
    if len(word) > 1:
        output_words.append(word.lower())
    # maybe_more_words = words.split('/\s+|\(/g')
    # for word in maybe_more_words:

f = open("english-cmu-reformat.txt", "w+")
f.write('\n'.join(output_words))
