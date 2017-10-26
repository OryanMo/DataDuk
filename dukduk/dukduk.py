from pandas import read_csv
import pandas as pd
import re
import nltk
import time
import operator
from nltk.corpus import stopwords
import numpy as np
import pickle
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

abstract_path = "../multindex.csv"
pages_path = "../allwords.csv"

prefix = "https://en.wikipedia.org/wiki/"
SINGLE_PAGE = 1


def disambiguate_page(entity, text, abstracts, label, index):
    try:
        names = abstracts.get_names_for_term(entity)
    except:
        return entity, 'nan'

    text = list(set(text.split()))

    # entry_counter = {i: 0 for i in names.index.tolist()}

    # for word in text:
    # for entry in names.iterrows():
    # print(entry)
    # entry_counter[entry[0]] += count_word(word, entry[1].values[0])

    # max_entry = max(entry_counter.items(), key=operator.itemgetter(1))[0]

    #withouf tfidf
    counts = []
    reg = "\\b" + "\\b|\\b".join(text) + "\\b"
    for name in names:
        counts.append({name: lenr(e.findall(reg, abstracts.get_abstract_for_name(name)))})



    # with tfidf
    # f = open("tfs_training.p", "rb")
    # tfs = pickle.load(f)
    # g = open("tfidf_training.p", "rb")
    # tfidf = pickle.load(g)
    # features = tfidf.get_feature_names()
    # counts = np.zeros((len(entries), 1))
    # for word in text:
    #     entity_index = features.index(word) if word in features else -1
    #     if entity_index >= 0:
    #         entity_tfidf = tfs[index, entity_index]
    #     else:
    #         entity_tfidf = 1
    #     counts += (entity_tfidf**2) * np.array([entries['Abstract'].str.count(word)]).T
    # if pd.isnull(label):
    #     print(counts)

    maxkey = max(counts.iteritems(), key=operator.itemgetter(1))[0]
    maxval = max(counts.values())
    if maxval < 3 or pd.isnull(maxval):
        max_entry = np.nan
        link = np.nan
    else:
        # print("======")
        # print(counts)
        # print("======")
        # print(counts.argmax())
        # print("======")
        # print(entries.loc[counts.argmax()])
        max_entry = maxkey
        link = prefix + max_entry

    return max_entry, link


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def count_word(word, abstract):
    if pd.isnull(abstract):
        return 0
    return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), abstract))


# remove label!
def entity_to_page(entity, text, abstracts=None, label=None, index=-1):
    if abstracts is None:
        abstracts = read_csv(abstract_path, encoding="utf-8", index_col=["Entity", "Name"])
        abstracts['Abstract'] = abstracts['Abstract'].str.lower()

    # stopswords = set(stopwords.words('english'))
    # abstracts["text"] = abstracts["text"].apply(lambda x: " ".join(word for word in x.split() if word.lower() not in stopwords))

    # pages = read_csv(pages_path, names=["entry"])

    # Check entity exist

    # Check whether disambiguation is needed
    if check_entity_single_page(entity, abstracts):
        return ("word", prefix + entity)
    # disambiguate term
    else:
        return disambiguate_page(entity, text, abstracts, label, index)
        # return {entity: "entity doesn't exists"}


def check_entity_exists(word, pages):
    return word in pages.entry.values


def check_entity_single_page(entity, abstracts):
    try:
        ret = len(abstracts.get_names_for_term(entity)) == SINGLE_PAGE
        return ret
    except:
        return False


def main():
    entity = ""
    text = ""
    entity_to_page(entity, text)



if __name__ == "__main__":
    main()
