from tkinter import Tk
import tkinter.filedialog as fd

from tqdm import tqdm
from time import sleep

import input
import Keyword_Extract


def get_files():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    # show an "Open" dialog box and return the path to the selected file
    files = fd.askopenfilenames(title='Choose files to upload')
    list_files = list(files)
    Tk().destroy()
    return list_files


if __name__ == "__main__":
    list_files = get_files()
    # get existing files and compare to see if file is already exists and  remove as needed

    no_of_files = len(list_files)
    text_from_files = []
    if no_of_files != 0:
        for i in tqdm(range(0, no_of_files), desc="Progress: "):

            # call to text extract

            text = input.filechecker(list_files[i])

            # call to keyword extract and get json
            json_array = Keyword_Extract.get_keywords_KeyBert(
                text, list_files[i])
            print(json_array)

            # call to index json into respective index files

            sleep(.4)
