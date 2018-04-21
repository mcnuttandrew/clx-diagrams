# -*- coding: utf-8 -*-
import nltk
import random
from utils import read_in_corpus
from mutual_information import compute_bigram_and_unigram_mutual_info

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

    # for sus_word in suspected_words:
    #     print "Word {0}".format(sus_word["word"])
    #     print sus_word["sub_words"]
    found_words = {}
    for sus_word in suspected_words:
        found_words[sus_word["word"]] = True

    non_compounds = []
    compounds = []
    for word in input_corpus:
        if word in found_words:
            compounds.append(word)
        else:
            non_compounds.append(word)


    base_gold_check(lang_dict, found_words)

    return (compounds, non_compounds)

def base_gold_check(eng_dict, found_words):
    count = 0
    gold_standard = read_in_corpus('./data/english-compound-gold-standard.txt')
    not_found = []
    for word in gold_standard:
        if word in found_words:
            count += 1
        else:
            if word in eng_dict:
                not_found.append(word)
    print "Found {0}/{1} -> word in dict / word in gold standard".format(count, len(gold_standard))
    print "The following words from the gold standard were not found in the input dictinary: {0}".format(
        ', '.join(not_found)
    )


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
        letter_a = word[idx]
        letter_b = word[idx + 1] if idx < (len(word) - 1) else ' '
        pair = (letter_a + letter_b)
        mutual_info_val = mutual_info[pair]
        if mutual_info_val < minimizing_val:
            minimizing_val = mutual_info_val
            minimizing_idx = idx
    return float("{0:.2f}".format((minimizing_idx + 0.0) / len(word)))

def compund_features(word):
    """
    convert a word into a format to give to the classifer
    """
    word_len = len(word)
    return {
        # 'last_letter': word[-1],
        # 'word_length': word_len,
        # 'first_letter': word[0],
        # 'num_vowels': num_values(word),
        'minimizing_fraction': find_index_of_most_negative_mutual_info(word),
        # 'middle_letter': word[(word_len - 1) / 2 if (word_len % 2) else word_len / 2],
        # maximize negative mutual information
        # 'txns': consonent_to_vowel_transitions_fraction(word)
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
    train_set, test_set = featuresets[500:], featuresets[:500]

    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    return classifier

def test_classifer(classifier):
    """
    test a classifier
    """
    test_cases = [
        ('bathhouse', True),
        ('fuck', False),
        ('fuckhead', True),
        ('biology', False),
        ('television', False)
        ]
    # test_cases = [('mammutwörter', True), ('backpfeifengesicht', True), ('heute', False)]
    for word, expected in test_cases:
        print "{0}: classfied as {1}, expected {2}. \n CLASSIFIER INPUT {3}".format(
            word,
            classifier.classify(compund_features(word)),
            'compound' if expected else 'non compound',
            compund_features(word)
            )
    # for idx in range(0, len(test_cases)):
    #     c = test_cases[idx]
    #     # expected = 'compound' if else 'non compound'
    #     # found = 'compound' if (classifier.classify(compund_features(case[0]) == 'compound') else 'non compound'
    #     print "{0}: classfied as {1}, expected {2}".format(c[0], classifier.classify(compund_features(c[0]), c[1])
    print ""
    # print classifier.classify(compund_features('fuck'))
    # print classifier.classify(compund_features('fuckhead'))
    print classifier.show_most_informative_features(5)


def test_english_classifer(classifier):
    """
    some specific testing for the english classifier, makes use of the gold standard list
    """
    gold_standard = read_in_corpus('./data/english-compound-gold-standard.txt')
    gold_count = 0
    gold_misses = []
    for word in gold_standard:
        if classifier.classify(compund_features(word)) == 'compound':
            gold_count += 1
        else:
            gold_misses.append(word)
    print "GOLD CHECK: {0}/{1}".format(gold_count, len(gold_standard))
    print "The following words from the gold standard were expected to be compound, were labeled as not: {0}".format(
        ', '.join(gold_misses)
    )

def main():
    """
    main method
    """
    global mutual_info
    mutual_info = compute_bigram_and_unigram_mutual_info('./data/eng-dictionary.txt')
    compounds, non_compounds = build_training_data('./data/eng-dictionary.txt')
    classifer = train_model(compounds, non_compounds)
    test_classifer(classifer)
    test_english_classifer(classifer)

    # compounds, non_compounds = build_training_data('./german-dict-final.txt')
    # print compounds
    # classifer = train_model(compounds, non_compounds)
    # test_classifer(classifer)
    # test_english_classifer(classifer)

    # compounds, non_compounds = build_training_data('./thai-wordlist.txt')
    # classifer = train_model(compounds, non_compounds)
    # test_classifer(classifer)
    # test_english_classifer(classifer)

if __name__ == "__main__":
    main()
