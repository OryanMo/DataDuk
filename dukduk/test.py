from pandas import read_csv
from dukduk import entity_to_page
import dukduk
from nltk.corpus import stopwords
import re
import pandas as pd
import numpy as np
import nltk
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from dataduk import Abstracts

# abstract_path = "../multindex.csv"


def main():
    train = read_csv("NEDDataHack2017_train.tsv", names=["entity", "disambig_term", "text", "wikipedia_link"], sep='\t',
                     header=0)
    stopswords = set(stopwords.words('english'))
    train["text"] = train["text"].apply(
        lambda x: " ".join(word.lower() for word in x.split() if word.lower() not in stopswords))
    train["text"] = train["text"].str.replace("|".join(map(re.escape, list("<>?)(.,[]{}*/+=-_"))), " ")
    train['text'] = train.apply(lambda x: x["text"].replace(x["entity"], " "), axis=1)

    # train.dropna(axis=0, how='any', inplace=True)

    # abstracts = read_csv(abstract_path, encoding="utf-8", index_col=["Entity", "Name"])
    abstracts = Abstracts("../test.csv")
    abstracts.df['Abstract'] = abstracts.df['Abstract'].str.lower()

    count = 0
    index = 0
    for row in train.iterrows():
        # print(row)
        index += 1
        print(row[1]['disambig_term'])
        print("answer:  {}".format(row[1]['wikipedia_link']))
        print("\ncontext: {}".format(row[1]['text']))
        res = entity_to_page(row[1]['disambig_term'], row[1]['text'], abstracts, row[1]['wikipedia_link'], row[0] - 1)
        print("\npredict: {}".format(res[1]))
        ans = row[1]['wikipedia_link']
        if res[1] == ans:
            count += 1
            # print("predict: {}".format(res[1]))
            # print("answer:  {}".format(row[1]['wikipedia_link']))
            # if index % 10 == 0:row[1]['wikipedia_link']
        elif pd.isnull(res[1]) and pd.isnull(ans):
            count += 1
        print("=============================================")
        if index == 100:
            break

    print(count, "/", index)


def calculate_tfidf():
    df = pd.read_csv("NEDDataHack2017_train.tsv", header=0, sep="\t")
    textCol = df['text'].str.lower().to_string(index=False)
    textCol = str.replace(textCol, '<p>', " ")
    import string
    translator = str.maketrans('', '', string.punctuation)
    textColNoPunct = textCol.translate(translator)
    token_dict = {}
    textColLines = textCol.split('\n')
    for linenum, text in enumerate(textColLines):
        token_dict[linenum] = text.strip(' \t')
    tfidf = TfidfVectorizer(tokenizer=dukduk.tokenize, stop_words='english', analyzer='word')
    tfs = tfidf.fit_transform(token_dict.values())
    pickle.dump(tfs, open("tfs_training.p", "wb"))
    pickle.dump(tfidf, open("tfidf_training.p", "wb"))

    exit()


if __name__ == "__main__":
    main()
