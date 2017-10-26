from gensim.models.keyedvectors import KeyedVectors

def read_model():
    word2vec_filename = "../word2vec.6B.50d.txt"
    model = KeyedVectors.load_word2vec_format(word2vec_filename, binary=False)
    return model

def is_similar(model, threshold, word1, word2):
    try:
        similarity = model.similarity(word1, word2)
        if similarity > threshold:
            return True
        else:
            return False
    except KeyError:
        return False

def count_similar_words(model, threshold, sentence1, sentence2):
    counter = 0
    for word1 in sentence1:
        for word2 in sentence2:
            if is_similar(model, threshold, word1, word2):
                counter += 1
    return counter