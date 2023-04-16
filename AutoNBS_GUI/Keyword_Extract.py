
import time
import json
import spacy
from keybert import KeyBERT
kw_model = KeyBERT()
nlp = spacy.load("en_core_web_sm")  # loads spacy's english core library
sw_spacy = nlp.Defaults.stop_words


def get_keywords_KeyBert(text, doc_location, filetype):

    try:
        keys = kw_model.extract_keywords(
            docs=text,
            keyphrase_ngram_range=(1, 1),
            top_n=int(0.33*len(text))
        )

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
        if key[0] not in sw_spacy and key[1] > 0.2:
            keyDict["keyword"] = key[0]
            keyDict["score"] = key[1]
            keywords.append(keyDict)

    dict["keywords_array"] = keywords
    array.append(dict)
    return json.dumps(array)
