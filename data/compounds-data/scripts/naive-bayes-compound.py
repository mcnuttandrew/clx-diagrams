# -*- coding: utf-8 -*-
import nltk
import random
from utils import read_in_corpus
from mutual_information import compute_bigram_and_unigram_mutual_info

# thai
# COMPOUND_GOLD_STANDARD = './data/Thai_compound_words.txt'
# LANG_DICTIONARY = './data/thai-wordlist.txt'
# english
COMPOUND_GOLD_STANDARD = './data/english_compound_words.txt'
LANG_DICTIONARY = './data/eng-dictionary.txt'
# LANG_DICTIONARY = './data/english-cmu-reformat.txt'
# german
# COMPOUND_GOLD_STANDARD = './data/German_compound_words.txt'
# LANG_DICTIONARY = './data/german-dict-final.txt'
# dutch
# COMPOUND_GOLD_STANDARD = './data/Dutch_compound_words.txt'
# LANG_DICTIONARY = './data/dutch-dictionary.txt'
# Finnish
# COMPOUND_GOLD_STANDARD = './data/Finnish_compound_words.txt'
# LANG_DICTIONARY = './data/finnish-dictionary.txt'

def read_in_corpus(filename):
    """
    Read and format corpus for consumption. returns a list of strings
    """
    with open(filename) as file_content:
        # unsure if strig is correct
        return [x.lower().strip() for x in file_content.readlines()]

def build_training_data(filename):
    input_corpus = read_in_corpus(filename)
    # build dictionary
    lang_dict = {}
    for word in input_corpus:
        lang_dict[word] = True
    # evaluate whether or not every word in dictionary is a compound

    suspected_words = []
    for word in input_corpus:
        word_with_associates = {
            "word": word,
            "sub_words": []
        }
        if len(word) < 4:
            continue
        # naive algorithm
        for idx in range(2, len(word) - 2):
            left_word = word[0:idx]
            right_word = word[idx:len(word)]
            if (left_word in lang_dict) and (right_word in lang_dict):
                word_with_associates['sub_words'].append((left_word, right_word))
        if len(word_with_associates['sub_words']):
            suspected_words.append(word_with_associates)

    found_words = {}
    for sus_word in suspected_words:
        found_words[sus_word["word"]] = True

    non_compounds = []
    compounds = []
    for word in input_corpus:
        if len(word) == 0:
            continue
        if word in found_words:
            compounds.append(word)
        else:
            non_compounds.append(word)


    # should use this as a filter against false positive/false negatives?
    # base_gold_check(lang_dict, found_words)

    return (compounds, non_compounds)

def base_gold_check(eng_dict, found_words):
    count = 0
    gold_standard = read_in_corpus(COMPOUND_GOLD_STANDARD)
    not_found = []
    for word in gold_standard:
        # if the word was in the predicated set cool count it
        if word in found_words:
            count += 1
        else:
            # if the word was not in the predicated set but was present in the dictionaty we missed it
            if word in eng_dict:
                not_found.append(word)

    compounds_known_to_be_in_dict = 0
    for word in gold_standard:
        if word in eng_dict:
            compounds_known_to_be_in_dict += 1
    print "The naive cutting technique picked up {0}/{1} known compounds that were present in the original diction".format(count, compounds_known_to_be_in_dict)
    print "It missed: {0}".format(', '.join(not_found))


# from nltk.corpus import names


vowels = ['a', 'e', 'i', 'o', 'u']
def num_values(word):
    """
    count the number of vowels in a word
    """
    count_vowls = 0
    for letter in word:
        if letter in vowels:
            count_vowls += 1
    return count_vowls

def consonent_to_vowel_transitions_fraction(word):
    """
    count the number of consonent vowel transitions in a word
    """
    transitions = 0
    for idx in range(0, len(word)):
        if word[idx] in vowels and word[idx] not in vowels:
            transitions += 1
    return transitions# / len(word)

def find_index_of_most_negative_mutual_info(word):
    """
    find where in the word the most negative pmi occurs
    """
    minimizing_idx = 0
    minimizing_val = 0
    for idx in range(0, len(word)):
        letter_a = word[idx] if idx >= 0 else '#'
        letter_b = word[idx + 1] if idx < (len(word) - 1) else ' '
        pair = (letter_a + letter_b)
        mutual_info_val = mutual_info[pair] if pair in mutual_info else -10000
        if mutual_info_val < minimizing_val:
            minimizing_val = mutual_info_val
            minimizing_idx = idx
    return (minimizing_idx + 0.0) / len(word)

def greatest_number_of_repeated_chars(word):
    char_counts = {}
    for letter in word:
        if not letter in char_counts:
            char_counts[letter] = 0
        char_counts[letter] += 1

    max_char = ''
    max_count = -1
    for char, count in char_counts.items():
        if count > max_count:
            max_count = count
            max_char = char
    return max_count

def compund_features(word):
    """
    convert a word into a format to give to the classifier
    """
    word_len = len(word)
    word_mid = (word_len - 1) / 2 if (word_len % 2) else word_len / 2
    return {

        # 'word': word,
        # 'last_letter': word[-1],
        # 'word_length': word_len,
        # 'first_letter': word[0],
        # 'num_vowels': num_values(word),
        # 'minimizing_fraction': find_index_of_most_negative_mutual_info(word),
        'middle_letter': word[word_mid],
        'middle_pair': word[word_mid-1:word_mid+1],
        # 'middle_pair_2': mutual_info[word[word_mid:word_mid+2]],
        'middle_pair_2': word[word_mid-2:   word_mid],
        # 'txns': consonent_to_vowel_transitions_fraction(word),
        # 'max_char': greatest_number_of_repeated_chars(word)
    }


def train_model(compounds, non_compounds):
    """
    train a naive baysian model for classifing
    """
    labeled_words = (
        [(word, 'compound') for word in compounds] +
        [(word, 'not_compound') for word in non_compounds]
    )

    random.shuffle(labeled_words)
    featuresets = [(compund_features(n), word_type) for (n, word_type) in labeled_words]
    train_set, test_set = featuresets[3000:], featuresets[:3000]

    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("CLASSIFIER ACCURACY {0}".format(nltk.classify.accuracy(classifier, test_set)))
    return classifier



def test_classifier(classifier, filename):
    """
    compare classifier behaviour with collection of known compounds
    """
    gold_standard_a = read_in_corpus(filename)
    # gold_standard_b = read_in_corpus('./data/German_compound_words.txt')
    gold_standard = gold_standard_a# + gold_standard_b
    gold_count = 0
    gold_misses = []
    for word in gold_standard:
        if classifier.classify(compund_features(word)) == 'compound':
            gold_count += 1
        else:
            gold_misses.append(word)
    print "Classifier correct categorizedly {0}/{1} known compounds".format(gold_count, len(gold_standard))
    print "The first 500 it missed were {0}".format(', '.join(gold_misses[:500]))

def main():
    """
    main method
    """
    global mutual_info
    print "\n-------------------\nBUILDING TRAINING DATA\n-------------------\n"
    mutual_info = compute_bigram_and_unigram_mutual_info(LANG_DICTIONARY)
    compounds_a, non_compounds_a = build_training_data(LANG_DICTIONARY)
    # COMPOUND_GOLD_STANDARD = './data/German_compound_words.txt'
    # LANG_DICTIONARY = './data/german-dict-final.txt'
    # compounds_b, non_compounds_b = build_training_data('./data/german-dict-final.txt')
    compounds = compounds_a# + compounds_b
    non_compounds = non_compounds_a# + non_compounds_b
    print "\n-------------------\nBUILDING CLASSIFIER\n-------------------\n"
    classifier = train_model(compounds, non_compounds)
    print "\n-------------------\nTESTING CLASSIFIER \n-------------------\n"
    print classifier.show_most_informative_features(20)
    test_classifier(classifier, COMPOUND_GOLD_STANDARD)

if __name__ == "__main__":
    main()
