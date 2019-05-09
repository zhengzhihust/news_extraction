# -*- coding: utf-8 -*-
'''
@File    : algosettings.py
@Datetime: 2019/5/7
'''

CONFIG = {
    'pretrain': './pretrained/zhwiki_sohu_100d.model',
    'vector_path': './word2vec/word2vec_100d.model',
    'sentences_file': './sentences.txt',
}


class Config:
    def __init__(self):
        for name, value in CONFIG.items():
            setattr(self, name, value)
