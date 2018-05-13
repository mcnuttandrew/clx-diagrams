from kshape.core import kshape, zscore
from utils import read_in_corpus
from mutual_information import compute_bigram_and_unigram_mutual_info

LANG_DICTIONARY = './data/eng-dictionary.txt'

def distribution_for_word(mutual_info, word):
    distro = []
    for i in range(0, len(word) - 1):
        distro.append(mutual_info[word[i:(i+2)]])
    return distro

def generate_mutual_info_distributions(lang_dict):
    mutual_info = compute_bigram_and_unigram_mutual_info(lang_dict)
    corp = read_in_corpus(read_in_corpus)
    distribution_to_word = {}
    distros = []
    for word in corp:
        distro = distribution_for_word(mutual_info, word)



def main():
    """
    main method
    """
    generate_mutual_info_distributions(LANG_DICTIONARY)

if __name__ == "__main__":
    main()
