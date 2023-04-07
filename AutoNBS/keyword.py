from keybert import KeyBERT
import json

kw_model = KeyBERT()

test = """Supervised learning is the machine learning task of learning a function that
        maps an input to an output based on example input-output pairs. It infers a
        function from labeled training data consisting of a set of training examples.
        In supervised learning, each example is a pair consisting of an input object
        (typically a vector) and a desired output value (also called the supervisory signal). 
        A supervised learning algorithm analyzes the training data and produces an inferred function, 
        which can be used for mapping new examples. An optimal scenario will allow for the 
        algorithm to correctly determine the class labels for unseen instances. This requires 
        the learning algorithm to generalize from the training data to unseen situations in a 
        'reasonable' way (see inductive bias)."""


def get_keywords_KeyBert(text):
    keys = kw_model.extract_keywords(
        docs=text,
        keyphrase_ngram_range=(1, 1),
        top_n=int(0.41*len(text))
    )
    return keys


# {
#     "doc_id": "640cb88a5eff2f53842b3680",
#     "doc_loc": "38.202.060/0001-60",
#     "keywords_array": [
#       {
#         "keyword": "Newman",
#         "score": 3
#       },
#       {
#         "keyword": "Bryant",
#         "score": 6
#       },
#       {
#         "keyword": "Baile",
#         "score": 2
#       },
#       {
#         "keyword": "Kramer",
#         "score": 10
#       },
#       {
#         "keyword": "Boyd",
#         "score": 3
#       }
#     ]
#   }

def generate_json_keywords(keys):
    dict = {}
    dict["doc_loc"] = "dsklfjkdalsjfaklds"
    keywords = []
    for key in keys:
        keyDict = {}
        keyDict["keyword"] = key[0]
        keyDict["score"] = key[1]
        keywords.append(keyDict)

    dict["keywords_array"] = keywords
    return json.load(dict)
