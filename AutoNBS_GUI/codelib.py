from tkinter import Tk
import tkinter.filedialog as fd

def getFiles():
    # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    win= Tk()
    win.attributes('-topmost',True, '-alpha',0)
    # show an "Open" dialog box and return the path to the selected file
    # win.withdraw()
    files = fd.askopenfilenames(title='Choose files to upload')
    list_files = list(files)
    win.destroy()
    return list_files


def checkDuplicate(list_files):
    import os

    # print(list_files)

    if "doc_info.parquet" in os.listdir("./index"):
        import polars as pl
        df = pl.scan_parquet('./index/doc_info.parquet')
        existing_files = list(
            df.select(pl.col('location')).collect().to_dict()['location'])
        intersection = list(set(existing_files).intersection(set(list_files)))
        for item in intersection:
            if item in list_files:
                list_files.remove(item)
    return list_files


def indexFiles(list_files):
    import Input_Module
    import Keyword_Extract
    import Index_Module
    from tqdm import tqdm
    import time

    no_of_files = len(list_files)
    msg = ""
    if no_of_files != 0:
        for i in tqdm(range(0, no_of_files), desc="Progress: "):

            # call to text extract

            text, filetype = Input_Module.filechecker(list_files[i])
            if text == None:
                continue
            # call to keyword extract and get json

            json_array = Keyword_Extract.get_keywords_KeyBert(
                text, list_files[i], filetype)
            if json_array == None:
                continue

            # call to index json into respective index files
            try:
                Index_Module.create_keyword_index(json_array)
            except Exception as e:
                # with open('./log.txt', 'a') as f:
                #     f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
                #     f.close()
                msg = "Indexation failed for this file hence skipped"
                print("Indexation failed for this file hence skipped")
    else:
        msg = "Given files are already Indexed"
        print("Given files are already Indexed")
    
    return msg