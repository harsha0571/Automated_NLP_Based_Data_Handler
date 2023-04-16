
import time
import json
import spacy
from keybert import KeyBERT

import nltk
from nltk.corpus import brown
from collections import defaultdict
from nltk.stem.porter import *

nltk.download('brown')

vocab = set(brown.words())
stemmer = PorterStemmer()
d = defaultdict(set)
for v in vocab:
    d[stemmer.stem(v)].add(v)

kw_model = KeyBERT()
nlp = spacy.load("en_core_web_sm")  # loads spacy's english core library
sw_spacy = nlp.Defaults.stop_words

def possible_root_words(word):

    possible = d[stemmer.stem(word)]
    possible = [p.lower() for p in possible]
    return possible

def tuple_to_list(tuples):
    keys = []
    index = []
    for i in range(len(tuples)):
        key = []
        
        key.append(tuples[i][0])
        key.append(tuples[i][1])
        
        keys.append(key)
        index.append(tuples[i][0])
    return keys , index

def list_to_tuple(lst):
    keys=[]
    for i in range(len(lst)):
        key = (lst[i][0],lst[i][1])
        keys.append(key)
    return keys

def stemming_lemmatization(idx,tpl):
    result = []
    for i in range(len(idx)):
        try:
            temp = possible_root_words(idx[i])
            root = temp[0]
            for t in temp:
                if len(t) < len(root):
                    root = t
            # print("root word: ",t)
            max_score = -1
            for i in range(len(idx)):
                if idx[i] in temp:
                    score = tpl[i][1]
                    if score>max_score:
                        max_score = score
            result.append([root , max_score])
        except:
            result.append([tpl[i][0], tpl[i][1]])
    res = []
    for i in range(len(result)):
        if result[i] not in res:
            res.append(result[i])
    return list_to_tuple(res)

def get_keywords_KeyBert(text, doc_location, filetype):

    try:
        keys = kw_model.extract_keywords(
            docs=text,
            keyphrase_ngram_range=(1, 1),
            top_n=int(0.33*len(text))
        )

        tlp,idx = tuple_to_list(keys)
        keys = stemming_lemmatization(idx,tlp)
        
        if filetype == "img":
            from autocorrect import Speller
            for i, key in enumerate(keys):
                spell = Speller().get_candidates(key[0])
                if len(spell) == 1:
                    keys[i] = (spell[0][1], key[1])

        json_array = generate_json_keywords(keys, doc_location)
        return json_array
    except Exception as e:
        with open('./log.txt', 'a') as f:
            f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
            f.close()
        print("\nKeyword extraction failed hence skipped")


def generate_json_keywords(keys, doc_location):
    array = []
    dict = {}
    dict["doc_loc"] = doc_location
    keywords = []
    for key in keys:
        keyDict = {}
        if key[0] not in sw_spacy and key[1] > 0.01:
            keyDict["keyword"] = key[0]
            keyDict["score"] = key[1]
            keywords.append(keyDict)

    dict["keywords_array"] = keywords
    array.append(dict)
    return json.dumps(array)
