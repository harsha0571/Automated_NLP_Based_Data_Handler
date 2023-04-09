from tkinter import Tk
import tkinter.filedialog as fd

from tqdm import tqdm
import time
import os


def get_files():
    # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    win= Tk()
    win.attributes('-topmost',True, '-alpha',0)
    # show an "Open" dialog box and return the path to the selected file
    # win.withdraw()
    files = fd.askopenfilenames(title='Choose files to upload')
    list_files = list(files)
    win.destroy()
    return list_files


def index_files():

    list_files = get_files()
    print("\n Indexing Started......\n")
    print(list_files)
    # get existing files and compare to see if file is already exists and  remove as needed
    if "doc_info.parquet" in os.listdir("./AutoNBS/index"):
        import polars as pl
        df = pl.scan_parquet('./AutoNBS/index/doc_info.parquet')
        existing_files = list(
            df.select(pl.col('location')).collect().to_dict()['location'])
        intersection = list(set(existing_files).intersection(set(list_files)))
        for item in intersection:
            if item in list_files:
                list_files.remove(item)

    import Input_Module
    import Keyword_Extract
    import Index_Module

    no_of_files = len(list_files)

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
                with open('./AutoNBS/log.txt', 'a') as f:
                    f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
                    f.close()
                print("Indexation failed for this file hence skipped")
    else:
        print("Given files are already Indexed")


def search_files():

    import Search_Module

    search_parameters = input(
        "\n Enter Search Parameters (EX: test,india,red,building) :   ")
    print("\n")

    try:

        keywords_list = search_parameters.split(",")
        keywords_list = [word.strip().replace(" ", "")
                         for word in keywords_list]
        keywords_list = [key for key in keywords_list if key +
                         ".parquet" in os.listdir("./AutoNBS/keywords")]
        start = time.time()
        result = Search_Module.searchForDocuments(
            "./AutoNBS/keywords", keywords_list)
        end = time.time()

        print(result.select("location").to_numpy())
        print("Result fetched in :", end-start, "sec")

        Search_Module.updateSearchHistory(keywords_list)
    except Exception as e:
        with open('./AutoNBS/log.txt', 'a') as f:
            f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
            f.close()
        print("Search Failed")


if __name__ == "__main__":

    while True:

        select = int(input(
            """\n\n
   _____          __          _______ __________  _________
  /  _  \  __ ___/  |_  ____  \      \\______   \/   _____/
 /  /_\  \|  |  \   __\/  _ \ /   |   \|    |  _/\_____  \ 
/    |    \  |  /|  | (  <_> )    |    \    |   \/        \\
\____|__  /____/ |__|  \____/\____|__  /______  /_______  /
        \/                           \/       \/        \/ 

\n  1.Index new files\n  2.Search from indexed files\n  3.Exit\n  Enter your Choice: """))

        print("\n")
        if select == 1:
            index_files()
        if select == 2:
            search_files()
        if select == 3:
            break
