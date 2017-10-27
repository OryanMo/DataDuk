import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import time
import numpy as np

# self.df = pd.read_csv("test.csv", encoding="utf-8", index_col=["Term", "Name"])

abst_regex = "\"(.*)\""
name_regex = " <http://dbpedia.org/resource/(.*?)> .*$"
term_regex = "^<http://dbpedia.org/resource/(.*?)>"
link_prefix = "https://en.wikipedia.org/wiki/"

class Abstracts():
    def __init__(self, path):
        self.path = path
        self.df = pd.read_csv(self.path, encoding="utf-8", index_col=["Term", "Name"])
        # self.df.fillna(value=np.NaN, inplace=True)
        # self.df.to_csv(self.path, encoding="utf-8")

        # print("2-00349583094509@*#$_)(@#*$_)(@#*4")
        # time.sleep(5)
    def update_csv(self):
        try:
            print("Wow")
            self.df.to_csv(self.path, encoding="utf-8")
        except (KeyboardInterrupt, SystemExit):
            print("Wow after KeyboardInterrupt")
            self.df.to_csv(self.path, encoding="utf-8")

    def get_abstract_for_name(self, name):
        retval = self.df.loc[self.df.index.get_level_values(1) == name]["Abstract"]
        if retval.empty or retval.isnull().any():
            retval = self.get_abstract_for_name_web(name)
            if retval.strip() == "":
                retval = "NoVal"
            self.df.loc[self.df.index.get_level_values(1) == name, "Abstract"] = retval
            # self.update_csv()
        return self.df.loc[self.df.index.get_level_values(1) == name, "Abstract"]


    def get_names_for_term(self, term):
        retval = self.df.loc[self.df.index.get_level_values(0) == term]
        if len(retval) == 0 or retval.empty:
            retval = self.get_names_for_term_web(term)
            for name in retval:
                a = self.df.loc[(term, name), "Abstract"] = np.NaN

            self.update_csv()
        return retval

    def get_abstracts_for_term(self, term):
        retval = self.df.loc[self.df.index.get_level_values(0) == term]
        if len(retval) == 0:# or pd.isnull(retval) or retval.empty:
            retval = self.get_names_for_term_web(term)
        if retval["Abstract"].isnull().values.any():
            # self.df.drop("Abstract", level=1, inplace=True)
            # self.update_csv()
            for i, name in retval[retval["Abstract"].isnull()].iterrows():
                self.get_abstract_for_name(i[1]).values[0]
                # self.df.loc[self.df.index.get_level_values(1) == i[1], "Abstract"] = self.get_abstract_for_name(i[1])
            self.update_csv()
        return self.df.loc[self.df.index.get_level_values(0) == term]


    def get_abstract_for_term_and_name(self, term, name):
        return self.get_abstract_for_name(name)
        # retval = self.df.loc[term, name]["Abstract"].tolist()[0]
        # if retval == "":
        #     retval = get_abstract_for_name_web(name)
        #     self.df.loc[self.df.index.get_level_values(1) == name, "Abstract"] = retval
        #     update_csv()


    def get_names_for_term_ttl(self, term):
        f = open("Files/disambiguations_en.ttl", "r", encoding="utf-8")
        all_lines = f.readlines()
        f.close()

        sambigs = pd.Series(all_lines)
        wanted = sambigs[sambigs.str.startswith("<http://dbpedia.org/resource/" + term + ">")]
        return wanted.str.extract(name_regex).tolist()


    def get_abstract_for_name_ttl(self, names):
        names = list(names)

        f = open("Files/short_self.df_en.ttl", "r", encoding="utf-8")
        all_lines = f.readlines()
        f.close()

        sabsts = pd.Series(all_lines)
        list_names = ["<http://dbpedia.org/resource/" + term + ">" for term in names]
        wanted = sabsts[sabsts.str.startswith(tuple(list_names))]

        return wanted.str.extract(abst_regex).tolist()


    def get_abstract_for_name_web(self, name):
        content = requests.get(link_prefix + name).content
        soup = BeautifulSoup(content, "lxml")
        data = [i.getText() for i in soup.select(".mw-parser-output p")]
        return "\n".join(data)

    def get_names_for_term_web(self, term):
        content = requests.get(link_prefix + term).content
        soup = BeautifulSoup(content, "lxml")
        a = soup.select("div.mw-parser-output  ul  li  a")
        return pd.Series([i["href"].split("/")[-1] for i in a])