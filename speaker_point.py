# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:42:39 2019

@author: Yu-Yiyang
"""

from pyhanlp import *
from functools import lru_cache

# pyhanlp: see https://github.com/hankcs/HanLP, need java and Jpype

def parse_sentence(sentence):
    return HanLP.parseDependency(sentence)

def search_dependency(parsed_sentence):
    '''
    input: Chinese text parsed by parse_sentence
    return: {speaker: point}
    '''
    result = {}
    for word in parsed_sentence.iterator():
        if word.DEPREL == '主谓关系': #and word.HEAD.LEMMA是“说”的近义词
            #TODO: if word.LEMMA is 代词， 指代消解
            speaker_id = word.ID
            root_id = word.HEAD.ID
            result[word.LEMMA] = search(parsed_sentence, root_id, speaker_id) #word.LEMMA为发表观点的人
    return result           
            
def search(parsed_sentence, root_id, speaker_id):
    '''
    :root_id: id for "说"
    :speaker_id: speaker name word id
    :target_id: target word id, search whether it belong to "说"
    search the entire sentence, all tokens that belong to root and not belong to speaker is the result
    '''
    result = ''    
    for word in parsed_sentence.iterator():
        if check_word(parsed_sentence, root_id, speaker_id, word):
            result += word.LEMMA
    return result
        
@lru_cache(maxsize = 32)
def check_word(parsed_sentence, root_id, speaker_id, word):
    if word.ID in [speaker_id, 0]: return False
    if word.HEAD.ID == root_id: return True #找到
    return check_word(parsed_sentence, root_id, speaker_id, word.HEAD)