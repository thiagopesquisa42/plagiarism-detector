#!/usr/bin/env python

import os
import string
import sys
import xml.dom.minidom
import codecs
import re
from pandas import read_csv
from numpy import array, transpose
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, ExtraTreesClassifier
import scipy.spatial.distance as distance
# Const
# =====

DELETECHARS = ''.join([string.punctuation, string.whitespace])
STRING_PUNCTUATION = ''.join([string.punctuation])
STRING_WHITESPACE = ''.join([string.whitespace])
LENGTH = 50

def remove_especial_characters(text):
    text_result = "";
    for character in text:
        if(character not in STRING_PUNCTUATION):
            text_result += character
    return text_result

def tokenize_by_white_space(text):
    regex_rule = "|".join(STRING_WHITESPACE)
    return re.split(regex_rule,text)

def get_token_occurrency(token_list, token):
    return token_list.count(token)


# Carregando dados
database = read_csv(
    'C:/plagiarism_detector_files_base/'+'linearRegisters/annotations_evidences.csv',
    sep = ";", encoding = "ISO-8859-1")

database['tokensSource'] = [
    tokenize_by_white_space(
        remove_especial_characters(excerpt))
    for excerpt in database['excerptSourceText']]
database['tokensSuspicious'] = [
    tokenize_by_white_space(
        remove_especial_characters(excerpt))
    for excerpt in database['excerptSuspiciousText']]
database_length = len(database['isPlagiarism'])
database['tokens'] = [
    list(
        set().
            union(
                database['tokensSource'][index],
                database['tokensSuspicious'][index]))
    for index in range(0, database_length)]
database['tokensSource'] = [
    [
        get_token_occurrency(
            token_list = database['tokensSource'][index], 
            token = _token)
        for _token in database['tokens'][index]
    ]
    for index in range(0, database_length)]
database['tokensSuspicious'] = [
    [
        get_token_occurrency(
            token_list = database['tokensSuspicious'][index], 
            token = _token)
        for _token in database['tokens'][index]
    ]
    for index in range(0, database_length)]

#cauculando distancia do coseno
database['cosineDistance'] = [
    distance.cosine(
        database['tokensSource'][index],
        database['tokensSuspicious'][index])
    for index in range(0, database_length)]

#saving the data preprocessed
database.to_csv(
    'C:/plagiarism_detector_files_base/'+'linearRegisters/annotations_features.csv',
    sep = ";", encoding = "ISO-8859-1")
    
