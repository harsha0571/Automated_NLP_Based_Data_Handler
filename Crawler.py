from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
from nltk.stem.porter import *
from bs4 import BeautifulSoup
import spacy
import nltk
from nltk.corpus import brown

nltk.download('brown')  # downloads the large nltk corpus of words
nlp = spacy.load("en_core_web_sm")  # loads spacy's english core library
sw_spacy = nlp.Defaults.stop_words


# create list of all possible stemming for each root word  -> possible = d[stemmer.stem('letting')]

vocab = set(brown.words())
stemmer = PorterStemmer()
d = defaultdict(set)
for v in vocab:
    d[stemmer.stem(v)].add(v)

# check if given word is noun


def check_noun(word):
    doc = nlp(word)

    if(doc[0].tag_ == 'NNP'):
        return True
    else:
        return False

# remove stopwords from text


def remove_stopwords(text):
    res = []
    for word in text:
        if word not in sw_spacy:
            res.append(word)
    return res

# removes all special characters from string


def nospecial(text):
    import re
    text = re.sub("[^a-zA-Z0-9]+", "", text)
    return text

# spider function to crawl the ted talks website for articles to get title and the keywords from the meta tag


start_url = "https://www.ted.com/talks/olivia_vinckier_a_colorful_case_for_outside_the_box_thinking_on_identity"

# download and put the compatible chromedriver in this location

driver = webdriver.Chrome('./personalTests/chromedriver.exe')


def spider(url, titles, found):
    driver.get(url)
    timeout = 3
    try:
        # element_present = EC.presence_of_element_located(
        #     (By.ID, 'tabs--1--panel--0'))
        element_present = EC.presence_of_element_located(
            (By.ID, 'main'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.lower().split()
    key = soup.select("meta[name='keywords']")[0]['content'].lower().split(",")

    keywords = []

    for k in key:
        for word in k.split():
            if word not in keywords:
                keywords.append(word)

    result = []

    for i in range(0, len(title)):
        title[i] = nospecial(title[i])

    while("" in title):
        title.remove("")

    for t in ["ted", "talk"]:
        title.remove(t)

    for word in title:
        if check_noun(word) and word not in result:
            result.append(word)

    for word in title:
        if word in keywords and word not in result:
            result.append(word)

    for word in keywords:
        try:
            possible = d[stemmer.stem(word)]
            possible = [p.lower() for p in possible]
            for p in possible:
                if p in title and p not in result:
                    result.append(p)
        except:
            pass

    result = remove_stopwords(result)

    og_title = " ".join(t for t in title)

    if len(result) > 0 and og_title not in titles:
        titles.append(og_title)
        print(og_title)
        print(result)
        f = open('dataset.txt', 'a')
        f.write(og_title + "\t" + '_'.join(k for k in result) + "\n")
        f.close()

    divs = soup.find_all("a", {"class": "mb-5 block p-3"})
    base_url = "https://www.ted.com"
    for d in divs:
        href = d.get_attribute_list("href")
        if base_url+href[0] not in found:
            found.append(base_url+href[0])
            spider(base_url+href[0], titles, found)


spider(start_url, [], [start_url])
driver.close()
