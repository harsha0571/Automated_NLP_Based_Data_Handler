

# import warnings
# warnings.filterwarnings('ignore')
import time


def filetype(filename):
    import re
    s = re.findall(
        "^.*\.(jpg|JPG|doc|DOC|docx|DOCX|pdf|PDF|txt|TXT|png|PNG|JPEG|jpeg|wav|WAV|MP3|mp3)$", filename)
    return (" ".join(s))


def filechecker(filename):
    if filetype(filename) == "txt" or filetype(filename) == "TXT":
        return extract_text(filename), "txt"
    if filetype(filename) == "pdf" or filetype(filename) == "PDF":
        return extract_pdf(filename), "pdf"
    if filetype(filename) == "png" or filetype(filename) == "PNG" or filetype(filename) == "jpg" or filetype(
            filename) == "JPG" or filetype(filename) == "JPEG" or filetype(filename) == "jpeg":
        return extract_img(filename), "img"
    if filetype(filename) == "wav" or filetype(filename) == "WAV" or filetype(filename) == "mp3" or filetype(
            filename) == "MP3":
        return extract_aud(filename), "aud"
    if filetype(filename) == "doc" or filetype(filename) == "DOC" or filetype(filename) == "docx" or filetype(
            filename) == "DOCX":
        return extract_doc(filename), "doc"
    else:
        print("\nUnspported Filetype hence skipped")


def extract_pdf(filename):
    import pdfplumber
    try:
        with pdfplumber.open(filename) as doc:
            text = ""
            for page in doc.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        with open('l./log.txt', 'a') as f:
            f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
            f.close()
        print("\nfailed to extract text from this pdf hence skipped")


def get_text_image_tesseract(filename):
    from pytesseract import pytesseract
    pathToTesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.tesseract_cmd = pathToTesseract
    text = pytesseract.image_to_string(filename)
    return text


def extract_img(filename):
    import easyocr
    from brisque import BRISQUE
    from PIL import Image
    from numpy import asarray
    try:
        img = Image.open(filename)
        numpydata = asarray(img)
        obj = BRISQUE(url=False)
        score = obj.score(numpydata)
        if score <= 90:
            reader = easyocr.Reader(['en'])
            results = reader.readtext(filename, detail=0)
            text = "\n".join(results)
            return text

        else:
            try:
                print("\nusing pytesseract so accuracy might be lower")
                text = get_text_image_tesseract(filename)
                return text
            except Exception as e:
                with open('./log.txt', 'a') as f:
                    f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
                    f.close()
                print(
                    "\nAll text extraction methods failed hence this image hence skipped")

    except Exception as e:
        with open('./log.txt', 'a') as f:
            f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
            f.close()
        print("\nThe image has lots of noise, hence unsuitable for extraction of text")


def extract_aud(filename):
    import whisper
    try:
        model = whisper.load_model("../datasets/small.pt")
        result = model.transcribe(filename)
        return result["text"]
    except Exception as e:
        with open('./log.txt', 'a') as f:
            f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
            f.close()
        print("\nFailed to extract text from this audio file hence skipped")


def extract_doc(filename):
    import docx
    try:
        doc = docx.Document(filename)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        textFromDoc = '\n'.join(text)

        return textFromDoc
    except Exception as e:
        with open('./log.txt', 'a') as f:
            f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
            f.close()
        print("\nFailed to extract text from this document hence skipped")


def extract_text(filename):
    try:
        with open(filename) as f:
            contents = f.read()
        f.close()

        return contents
    except Exception as e:
        with open('./log.txt', 'a') as f:
            f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
            f.close()
        print("\nFailed to fetch text form this text file hence skipped")
