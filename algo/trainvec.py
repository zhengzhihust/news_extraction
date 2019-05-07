# -*- coding: utf-8 -*-
'''
@File    : trainvec.py
@Datetime: 2019/5/7
'''
import re

import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from hanziconv import HanziConv

from algo.algosettings import Config
from database.dbconn import Database


class Trainvec():

    def __init__(self, config):
        self.config = config
        self.vector_path = config.vector_path

        pretrain = config.pretrain
        self.model = Word2Vec.load(pretrain)
        self.sentences = []

    def train(self):
        self.model = Word2Vec(LineSentence('sentences.txt'), workers=32)
        self.model.save(self.vector_path)

    def get_data(self):

        db = Database()
        all_data = db.list_all_data()

        for data in all_data:
            content = HanziConv.toSimplified(data['content'])
            for seq in re.split(r'[\n。？！?!]+', content):
                sent = ' '.join(re.findall('[\w|\d]+', seq))
                sent = self._cut(sent)
                if len(sent) < 3:
                    continue
                self.sentences.append(sent)
        self._write_txt(self.sentences)
        return self.sentences

    @staticmethod
    def _write_txt(data):
        with open('sentences.txt', 'w', encoding='utf-8') as f:
            for n in data:
                f.write(' '.join(n) + '\n')

    @staticmethod
    def _cut(string):
        res = [i for i in list(jieba.cut(string)) if i != ' ']
        return res


if __name__ == '__main__':
    config = Config()
    p = Trainvec(config)
    p.get_data()
    p.train()
