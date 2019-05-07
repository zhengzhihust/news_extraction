# -*- coding: utf-8 -*-
'''
@File    : preprocess.py
@Datetime: 2019/5/7
'''
import pickle
from collections import defaultdict

from gensim.models import Word2Vec

from algo.algosettings import Config


class Preprocess():
    def __init__(self, config):
        self.vector_path = config.vector_path
        self.model = Word2Vec.load(self.vector_path)

    # @lru_cache(maxsize=2 ** 10)
    def search_similar_words(self, initial_words):
        """
            @initial_words are initial words we already know
            @model is the word2vec model
        """
        unseen = initial_words
        seen = defaultdict(int)
        max_size = 500  # could be greater
        while unseen and len(seen) < max_size:
            if len(seen) % 50 == 0:
                print('seen length : {}'.format(len(seen)))
            node = unseen.pop(0)
            new_expanding = [w for w, s in self.model.wv.most_similar(node, topn=20)]
            unseen += new_expanding
            seen[node] += 1
            # optimal: 1. score function could be revised
            # optimal: 2. using dymanic programming to reduce computing time
        return seen


if __name__ == '__main__':
    config = Config()
    test = Preprocess(config)
    initial_words = ['说', '声明']
    related_words = test.search_similar_words(initial_words)
    related_words = sorted(related_words.items(), key=lambda x: x[1], reverse=True)
    with open('./related_words.pkl', 'wb') as f:
        pickle.dump(related_words, f)
    print(related_words)
