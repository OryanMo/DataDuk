from pandas import read_csv
import pandas as pd
import re
import nltk
import time
import operator
from nltk.corpus import stopwords
import numpy as np
import pickle
import similarity as sm

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

abstract_path = "../multindex.csv"
pages_path = "../allwords.csv"

prefix = "https://en.wikipedia.org/wiki/"
SINGLE_PAGE = 1

def disambiguate_page_with_similarity(model, entity, text, abstracts, label, index):
    try:
        entries = abstracts.loc[entity]
    except:
        return entity, 'nan'
    max_count = -1
    for index, row in entries.iterrows():
        #print(index)
        #print(row)
        if not pd.isnull(row['Abstract']):
            abstract =  list(set(row['Abstract'].split()))
            count = sm.count_similar_words(model, 0.95, text, abstract)
            if (count > max_count):
                max_count = count
                max_entry = index

    if max_count < 5: # or pd.isnull(counts.argmax()):
        max_entry = np.nan
        link = np.nan
    else:
        # print("======")
        # print(counts)
        # print("======")
        # print(counts.argmax())
        # print("======")
        # print(entries.loc[counts.argmax()])
        # max_entry = entries.loc[counts.argmax()].name
        link = prefix + max_entry

    return max_entry, link



def disambiguate_page(entity, text, abstracts, label, index):
    try:
        entries = abstracts.loc[entity]
    except:
        return entity, 'nan'

    text = list(set(text.split()))

    # entry_counter = {i: 0 for i in entries.index.tolist()}

    # for word in text:
    # for entry in entries.iterrows():
    # print(entry)
    # entry_counter[entry[0]] += count_word(word, entry[1].values[0])

    # max_entry = max(entry_counter.items(), key=operator.itemgetter(1))[0]

    #withouf tfidf
    counts = entries['Abstract'].str.count("|".join(text))



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

    if counts.max() < 5 or pd.isnull(counts.argmax()):
        max_entry = np.nan
        link = np.nan
    else:
        # print("======")
        # print(counts)
        # print("======")
        # print(counts.argmax())
        # print("======")
        # print(entries.loc[counts.argmax()])
        max_entry = entries.loc[counts.argmax()].name
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
def entity_to_page(model, entity, text, abstracts=None, label=None, index=-1):
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
        return disambiguate_page_with_similarity(model, entity, text, abstracts, label, index)
        # return {entity: "entity doesn't exists"}


def check_entity_exists(word, pages):
    return word in pages.entry.values


def check_entity_single_page(entity, abstracts):
    try:
        ret = len(abstracts.loc[entity].shape) == SINGLE_PAGE
        return ret
    except:
        return False


def main():
    entity = ""
    text = ""
    entity_to_page(entity, text)



if __name__ == "__main__":
    main()
