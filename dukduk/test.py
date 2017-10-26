from pandas import read_csv
from dukduk.dukduk import entity_to_page


def main():
    train = read_csv("NEDDataHack2017_train.tsv", names=["entity", "disambig_term", "text", "wikipedia_link"], sep='\t')

    count = 0
    for row in train:
        res = entity_to_page(row.entity, row.text)
        if res == row.wikipedia_link:
            count += 1
    if count % 100 == 0:
        print(count / train.shape[0])


if __name__ == "__main__":
    main()
