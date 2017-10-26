from pandas import read_csv
import re
import operator

abstract_path = ""
pages_path = ""

prefix = "https://en.wikipedia.org/wiki/"
SINGLE_PAGE = 1


def disambiguate_page(entity, text, abstracts):
    entries = abstracts.loc[entity]
    entry_counter = {i.entry: 0 for i in entries}

    for word in text.split():
        for entry in entries:
            entry_counter[entry.entry] += count_word(word, entry.abstract)

    max_entry = max(entry_counter.items(), key=operator.itemgetter(1))[0]

    return {max_entry: entries[entries.entry == max_entry].wikipedia_link}


def count_word(word, abstract):
    return sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), abstract))


def entity_to_page(entity, text):
    abstracts = read_csv(abstract_path, names=["entity", "entry", "abstract", "wikipedia_link"])
    pages = read_csv(pages_path, names=["entry"])
    abstracts.set_index("index")

    # Check entity exist
    if not check_entity_exists(entity, pages):
        return "entity doesn't exists"
    # Check whether disambiguation is needed
    elif check_entity_single_page(entity, abstracts):
        return {"word": prefix + entity}
    # disambiguate term
    else:
        return disambiguate_page(entity, text, abstracts)


def check_entity_exists(word, pages):
    return word in pages.entry.values


def check_entity_single_page(entity, abstracts):
    return len(abstracts.loc[entity].shape) == SINGLE_PAGE


def main():
    entity = ""
    text = ""
    entity_to_page(entity, text)


if __name__ == "__main__":
    main()
