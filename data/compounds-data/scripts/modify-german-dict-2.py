def read_in_corpus(filename):
    """
    Read and format corpus for consumption. returns a list of strings
    """
    with open(filename) as file_content:
        # unsure if strig is correct
        return [x for x in file_content.readlines()]


lines = read_in_corpus('./german-dict-2.txt')
output_words = []
for line in lines:
    words = line.split(' ')[0]
    maybe_more_words = words.split(',')
    for word in maybe_more_words:
        output_words.append(word.lower())

f = open("german-dict-rewrite.txt", "w+")
f.write('\n'.join(output_words))
