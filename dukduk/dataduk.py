import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time

df = pd.read_csv("test.csv", encoding="utf-8", index_col=["Term", "Name"])

abst_regex = "\"(.*)\""
name_regex = " <http://dbpedia.org/resource/(.*?)> .*$"
term_regex = "^<http://dbpedia.org/resource/(.*?)>"
link_prefix = "https://en.wikipedia.org/wiki/"


def update_csv():
    df.to_csv("test.csv", encoding="utf-8")


def get_abstract_for_name(name):
    retval = df.loc[df.index.get_level_values(1) == name]["Abstract"].tolist()[0]
    if retval == "" or pd.isnull(retval):
        retval = get_abstract_for_name_web(name)
        df.loc[df.index.get_level_values(1) == name, "Abstract"] = retval
        update_csv()
    return retval


def get_names_for_term(term):
    retval = df.loc[df.index.get_level_values(0) == term].index.get_level_values(1).tolist()
    if len(retval) == 0 or pd.isnull(retval):
        retval = get_names_for_term_web(term)
        for name in retval:
            df.ix[(term, name), "Abstract"] = None

        update_csv()
    return retval


def get_abstract_for_term_and_name(term, name):
    return get_abstract_for_name(name)
    # retval = df.loc[term, name]["Abstract"].tolist()[0]
    # if retval == "":
    #     retval = get_abstract_for_name_web(name)
    #     df.loc[df.index.get_level_values(1) == name, "Abstract"] = retval
    #     update_csv()


def get_names_for_term_ttl(term):
    f = open("Files/disambiguations_en.ttl", "r", encoding="utf-8")
    all_lines = f.readlines()
    f.close()

    sambigs = pd.Series(all_lines)
    wanted = sambigs[sambigs.str.startswith("<http://dbpedia.org/resource/" + term + ">")]
    return wanted.str.extract(name_regex).tolist()


def get_abstract_for_name_ttl(names):
    names = list(names)

    f = open("Files/short_abstracts_en.ttl", "r", encoding="utf-8")
    all_lines = f.readlines()
    f.close()

    sabsts = pd.Series(all_lines)
    list_names = ["<http://dbpedia.org/resource/" + term + ">" for term in names]
    wanted = sabsts[sabsts.str.startswith(tuple(list_names))]

    return wanted.str.extract(abst_regex).tolist()


def get_abstract_for_name_web(name):
    content = requests.get(link_prefix + name).content
    soup = BeautifulSoup(content, "lxml")
    data = [i.getText() for i in soup.select(".mw-parser-output p")]
    return "\n".join(data)

def get_names_for_term_web(term):
    content = requests.get(link_prefix + term).content
    soup = BeautifulSoup(content, "lxml")
    a = soup.select("div.mw-parser-output > ul > li > a")
    return [i["href"].split("/")[-1] for i in a]