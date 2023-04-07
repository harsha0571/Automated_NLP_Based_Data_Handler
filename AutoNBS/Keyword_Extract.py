from keybert import KeyBERT
import json
import spacy

kw_model = KeyBERT()


nlp = spacy.load("en_core_web_sm")  # loads spacy's english core library
sw_spacy = nlp.Defaults.stop_words


def get_keywords_KeyBert(text, doc_location):
    try:
        keys = kw_model.extract_keywords(
            docs=text,
            keyphrase_ngram_range=(1, 1),
            top_n=int(0.41*len(text))
        )
        json_array = generate_json_keywords(keys, doc_location)
    except:
        print("Keyword extraction failed hence skipped")

    return json_array


def generate_json_keywords(keys, doc_location):
    array = []
    dict = {}
    dict["doc_loc"] = doc_location
    keywords = []
    for key in keys:
        keyDict = {}
        if key[0] not in sw_spacy:
            keyDict["keyword"] = key[0]
            keyDict["score"] = key[1]
            keywords.append(keyDict)

    dict["keywords_array"] = keywords
    array.append(dict)
    return json.dumps(array)
