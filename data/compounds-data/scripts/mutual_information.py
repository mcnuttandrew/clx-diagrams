from utils import read_in_corpus
from math import log


def compute_bigram_and_unigram_mutual_info(filename):
    """
    generate bigram and unigram counts for all letters in all words in an input corpus
    """
    # initial variables
    corpus = read_in_corpus(filename)
    # using ' ' as stop char, and '#' as start char
    unigrams = {
        ' ': 0,
        # '#': 0
    }
    unigram_count = 0
    bigrams = {}
    bigrams_count = 0

    # generate counts
    for word in corpus:
        # unigrams['#'] += 1
        # unigram_count += 1
        # start_pair = '#' + word[0]
        # if start_pair not in bigrams:
        #     bigrams[start_pair] = 0
        # bigrams[start_pair] += 1
        # bigrams_count += 1

        for idx in range(0, len(word)):
            letter = word[idx]
            if letter not in unigrams:
                unigrams[letter] = 0
            unigrams[letter] += 1
            unigram_count += 1
            # if idx < (len(word) - 1):
            second_letter = word[idx + 1] if idx < (len(word) - 1) else ' '
            pair = letter + second_letter
            if pair not in bigrams:
                bigrams[pair] = 0
            bigrams[pair] += 1
            bigrams_count += 1

        unigrams[' '] += 1
        unigram_count += 1

    # normalize counts to freqs
    for key, value in unigrams.items():
        unigrams[key] = (value + 0.0) / unigram_count
    for key, value in bigrams.items():
        bigrams[key] = (value + 0.0) / bigrams_count

    # build mutual information for input letter pair
    mutual_information_dict = {}
    for key, value in bigrams.items():
        prob_a = unigrams[key[0]]
        prob_b = unigrams[key[1]]
        prob_ab = bigrams[key]
        mutual_information_dict[key] = log(prob_ab) - log(prob_a)  - log(prob_b)
    return mutual_information_dict

def main():
    """
    main method
    """
    print compute_bigram_and_unigram_mutual_info("./data/eng-dictionary.txt")


if __name__ == "__main__":
    main()
