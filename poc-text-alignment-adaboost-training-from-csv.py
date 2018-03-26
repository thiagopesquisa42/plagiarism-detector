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
    'C:/plagiarism_detector_files_base/'+'linearRegisters/annotations_features.csv',
    sep = ";", encoding = "ISO-8859-1")

#CRIANDO OS CAMPOS SEPARADOS PARA FACILITAR ANÁLISES
ignored_attributes = [
    "excerptSourceOffsetFromBegin",
    "excerptSourceText",
    "excerptSourceLocationOfFile",
    "excerptSuspiciousOffsetFromBegin",
    "excerptSuspiciousText",
    "tokensSource",
    "tokensSuspicious",
    "excerptSuspiciousLocationOfFile"]
data = transpose(array([
            database["plagiarismClass"],
            database["excerptSourceLength"],
            database["excerptSuspiciousLength"],
            database["cosineDistance"]
        ])
    )

target = database['plagiarismClass']
features_names = [key for key in database.keys() if(key not in ignored_attributes)]

# Particiona a base de dados
X_train, X_test, y_train, y_test = train_test_split(
                            data, target, random_state=0)

clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Classificador Árvore de Decisão:\n")
print(classification_report(y_test, y_pred))

# ADABOOST com árvores baixas
ada = AdaBoostClassifier(DecisionTreeClassifier(splitter="random", 
                                                max_depth=4,
                                                min_samples_split=20, 
                                                min_samples_leaf=5), 
                         algorithm="SAMME", n_estimators=200)
ada.fit(X_train, y_train)
y_pred = ada.predict(X_test)
print("Classificador AdaBoost:\n AdaBoostClassifier(tree.DecisionTreeClassifier(max_depth=1), algorithm=\"SAMME\", n_estimators=200)\n")
print(classification_report(y_test, y_pred))

# # Random forest com 10 arvores
# clr = RandomForestClassifier(n_estimators=100)
# clr = clf.fit(X_train, y_train)
# y_pred = clr.predict(X_test)
# print("Classificador Random Forest:\n RandomForestClassifier(n_estimators=10)\n")
# print(classification_report(y_test, y_pred))

# # Random forest com heurísticas extremas
# cle = ExtraTreesClassifier(n_estimators=100)
# cle = cle.fit(X_train, y_train)
# y_pred = cle.predict(X_test)
# print("Classificador Extreme Tree:\n ExtraTreesClassifier(n_estimators=10)\n")
# print(classification_report(y_test, y_pred))
