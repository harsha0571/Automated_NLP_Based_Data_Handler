import re
import os
# import filecmp
import easyocr
import whisper
import pdfplumber
import warnings
import docx
from brisque import BRISQUE
from PIL import Image
from numpy import asarray
from pytesseract import pytesseract

warnings.filterwarnings('ignore')


def filetype(filename):
    s = re.findall(
        "^.*\.(jpg|JPG|doc|DOC|docx|DOCX|pdf|PDF|txt|TXT|png|PNG|JPEG|jpeg|wav|WAV|MP3|mp3)$", filename)
    return (" ".join(s))


def filechecker(filename):
    if filetype(filename) == "txt" or filetype(filename) == "TXT":
        return extract_text(filename)
    if filetype(filename) == "pdf" or filetype(filename) == "PDF":
        return extract_pdf(filename)
    if filetype(filename) == "png" or filetype(filename) == "PNG" or filetype(filename) == "jpg" or filetype(
            filename) == "JPG" or filetype(filename) == "JPEG" or filetype(filename) == "jpeg":
        return extract_img(filename)
    if filetype(filename) == "wav" or filetype(filename) == "WAV" or filetype(filename) == "mp3" or filetype(
            filename) == "MP3":
        return extract_aud(filename)
    if filetype(filename) == "doc" or filetype(filename) == "DOC" or filetype(filename) == "docx" or filetype(
            filename) == "DOCX":
        return extract_doc(filename)
    else:
        print("Unspported Filetype hence skipped")


def extract_pdf(filename):
    try:
        with pdfplumber.open(filename) as doc:
            text = ""
            for page in doc.pages:
                text += page.extract_text()
        return text
    except:
        print("failed to extract text from this pdf hence skipped")


def get_text_image_tesseract(filename):
    pathToTesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.tesseract_cmd = pathToTesseract
    text = pytesseract.image_to_string(filename)
    return text


def extract_img(filename):
    try:
        img = Image.open(filename)
        numpydata = asarray(img)
        obj = BRISQUE(url=False)
        score = obj.score(numpydata)
        if score <= 90:
            reader = easyocr.Reader(['en'])
            results = reader.readtext(filename, detail=0)
            tempTuple = os.path.splitext(filename)
            filename = tempTuple[0]
            text = "\n".join(results)
            return text

        else:
            try:
                print("using pytesseract so accuracy might be lower")
                text = get_text_image_tesseract(filename)
                return text
            except:
                print(
                    "All text extraction methods failed hence this image hence skipped")

    except:
        print("The image has lots of noise, hence unsuitable for extraction of text")


def extract_aud(filename):
    try:
        model = whisper.load_model("./datasets/small.pt")
        result = model.transcribe(filename)
        return result["text"]
    except Exception as e:
        print("Failed to extract text from this audio file hence skipped")


def extract_doc(filename):
    try:
        doc = docx.Document(filename)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        textFromDoc = '\n'.join(text)

        return textFromDoc
    except:
        print("Failed to extract text from this document hence skipped")


def extract_text(filename):
    try:
        with open(filename) as f:
            contents = f.read()
        f.close()

        return contents
    except:
        print("Failed to fetch text form this text file hence skipped")
