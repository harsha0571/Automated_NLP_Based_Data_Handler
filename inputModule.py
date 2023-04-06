import re
import os
import filecmp
import easyocr
import whisper
import pdfplumber
import warnings
import docx
from brisque import BRISQUE
from PIL import Image
from numpy import asarray

warnings.filterwarnings('ignore')


def file_input():
    filename = str(input("Enter the filename"))
    files = os.listdir()
    for file in files:
        if file != filename:
            if filecmp.cmp(filename, file):
                ch = input('Duplicate has been detected press Y to delete or any other key to keep the duplicate')
                if ch == "y" or "Y":
                    os.remove(file)
                    print("File with filename", file, "has been deleted")
                else:
                    continue
        else:
            filechecker(filename)


def filetype(filename):
    s = re.findall("^.*\.(jpg|JPG|doc|DOC|docx|DOCX|pdf|PDF|txt|TXT|png|PNG|JPEG|jpeg|wav|WAV|MP3|mp3)$", filename)
    return (" ".join(s))


def extract_pdf(filename):
    with pdfplumber.open(filename) as doc:
        text = ""
        for page in doc.pages:
            text += page.extract_text()
    tempTuple = os.path.splitext(filename)
    filename = tempTuple[0]
    with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
        f.write(text)
    print("PDF data converted to text file")


def extract_img(filename):
    try:
        img = Image.open(filename)
        numpydata = asarray(img)
        obj = BRISQUE(url=False)
        score = obj.score(numpydata)
        if score <=90:
            reader = easyocr.Reader(['en'])
            results = reader.readtext(filename, detail=0)
            tempTuple = os.path.splitext(filename)
            filename = tempTuple[0]
            with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
                for a in results:
                    f.write(a)
                    f.write("\n")
            print("Image data converted to text file ")
        else:
            print("The image file has lot of noise and is unsuitable for extraction of text")
    except:
        print("The image has lots of noise,hence unsuitable for extraction of text")


def extract_aud(filename):
    model = whisper.load_model("large.pt")
    result = model.transcribe(filename)
    tempTuple = os.path.splitext(filename)
    filename = tempTuple[0]
    with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
        f.write(result["text"])
    print("Audio data converted to text file")


def extract_doc(filename):
    doc = docx.Document(filename)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    text1 = '\n'.join(text)
    tempTuple = os.path.splitext(filename)
    filename = tempTuple[0]
    with open(f"{filename}.txt", 'w', encoding='utf-8') as f:
        f.write(text1)
    print("Doc data converted to text file")


def filechecker(filename):
    if filetype(filename) == "pdf" or filetype(filename) == "PDF":
        extract_pdf(filename)
    if filetype(filename) == "png" or filetype(filename) == "PNG" or filetype(filename) == "jpg" or filetype(
            filename) == "JPG" or filetype(filename) == "JPEG" or filetype(filename) == "jpeg":
        extract_img(filename)
    if filetype(filename) == "wav" or filetype(filename) == "WAV" or filetype(filename) == "mp3" or filetype(
            filename) == "MP3":
        extract_aud(filename)
    if filetype(filename) == "doc" or filetype(filename) == "DOC" or filetype(filename) == "docx" or filetype(
            filename) == "DOCX":
        extract_doc(filename)


while True:
    ch = input("Enter Y to continue and N to stop")
    if ch == "y" or ch == "Y":
        file_input()
    else:
        break

