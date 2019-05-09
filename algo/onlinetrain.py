# -*- coding: utf-8 -*-
'''
@File    : trainvec.py
@Datetime: 2019/5/7
'''
import os
import re

import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from hanziconv import HanziConv

from algo.algosettings import Config
from database.dbconn import Database
from utils.log import logger


class Onlinetrain():
    '''
    针对新闻语料库追加训练词向量
    '''

    def __init__(self, config):
        self.config = config
        self.vector_path = config.vector_path
        if not os.path.exists(self.vector_path):
            os.makedirs(self.vector_path)

        self.sentences_file = config.sentences_file

        pretrain = config.pretrain
        logger.info('loading word2vec model from {}'.format(pretrain))
        self.model = Word2Vec.load(pretrain)
        logger.info('succeed load model')

    def train(self):
        logger.info('start online training...')
        self.model.train(LineSentence(self.sentences_file), total_examples=self.model.corpus_count,
                         epochs=self.model.epochs)
        self.model.save(self.vector_path)
        logger.info('online training finished, model has saved in {}'.format(self.vector_path))

    def get_data(self):

        db = Database()
        all_data = db.list_data()

        if os.path.exists(self.sentences_file):
            os.remove(self.sentences_file)

        for data in all_data:
            content = HanziConv.toSimplified(data['content'])
            sent = ' '.join(re.findall('[\w|\d]+', content))
            sent = self._cut(sent)
            self._write_line(sent, self.sentences_file)
        return len(all_data)

    @staticmethod
    def _write_line(sentence, file):
        with open(file, 'a+', encoding='utf-8') as f:
            f.write(' '.join(sentence) + '\n')

    @staticmethod
    def _cut(string):
        res = [i for i in list(jieba.cut(string)) if i != ' ']
        return res


if __name__ == '__main__':
    config = Config()
    p = Onlinetrain(config)
    p.get_data()
    p.train()
