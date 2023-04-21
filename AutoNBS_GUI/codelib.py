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
    removed_files= []
    if "doc_info.parquet" in os.listdir("./index"):
        import polars as pl
        df = pl.scan_parquet('./index/doc_info.parquet')
        existing_files = list(
            df.select(pl.col('location')).collect().to_dict()['location'])
        intersection = list(set(existing_files).intersection(set(list_files)))
        for item in intersection:
            if item in list_files:
                removed_files.append(item)
                list_files.remove(item)
    return [list_files,removed_files]


def indexFiles(list_files):
    import Input_Module
    import Keyword_Extract
    import Index_Module
    from tqdm import tqdm
    import time
    keyUnique= []
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
                keyUnique= Index_Module.create_keyword_index(json_array)
            except Exception as e:
                # with open('./log.txt', 'a') as f:
                #     f.write('\n\n'+time.ctime()+"\n"+str(e)+"\n\n")
                #     f.close()
                msg = "Indexation failed for this file hence skipped"
                print("Indexation failed for this file hence skipped")
    else:
        msg = "Given files are already Indexed"
        print("Given files are already Indexed")
    
    return [msg, keyUnique]

def fetchAnalyticalData():
    import json
    f= open('./analyticsData/analysisData.json')
    inputData= json.load(f)
    import os
    if "doc_info.parquet" not in os.listdir('./index/'):
        inputData["totalDocs"]= 0
    else:
        import pyarrow.parquet as pq
        inputData["totalDocs"]= pq.read_metadata('./index/doc_info.parquet').num_rows
        import polars as pl
        df0= pl.scan_parquet('./index/doc_info.parquet').select(pl.col('location').str.extract(pattern= r"[.](\w+)"))
        df= df0.groupby("location").count().collect()
        df1= df0.tail(100).groupby("location").count().collect()

        for extension, count in df.iter_rows():
            if extension in ['txt', 'doc', 'pdf']:
                inputData["mediaFilesCount"]['text']+=count
            elif extension in ['img', 'png', 'jpg']:
                inputData["mediaFilesCount"]['image']+=count
            else:
                inputData["mediaFilesCount"]['audio']+=count

        # print(pl.read_parquet('./index/doc_info.parquet').select(pl.col('location').str.extract(pattern= r"[.](\w+)")))
        for extension, count in df1.iter_rows():
            if extension in ['txt', 'doc', 'pdf']:
                inputData["latestFilesAdded"][0]['text']+=count
            elif extension in ['img', 'png', 'jpg']:
                inputData["latestFilesAdded"][0]['image']+=count
            else:
                inputData["latestFilesAdded"][0]['audio']+=count
            inputData["latestFilesAdded"][1][extension]=count

        files= os.listdir('./keywords/')
        extensionList= list(set(df.select(pl.col('location')).to_series()))
        fileNames= [""]*len(files)
        freq= [0]*len(files) 
        for i in range(len(files)):
            fileNames[i]= files[i][:-8]
            freq[i]= pq.read_metadata('./keywords/'+files[i]).num_rows
        inputData['totalKeywords']= len(files)
        inputData['supportedFormats']= extensionList
        keyFrame= pl.from_dict({'key': fileNames, 'freq': freq}).sort(by= 'freq', descending=True)[:100]
        keyFrame= keyFrame.to_dict()
        inputData['mostCommonKeywords']= keyFrame
        # print(inputData['mostCommonKeywords']['freq'])
        import numpy as np
        if 'searchHistory.parquet' in os.listdir('./history/'):
            df= pl.scan_parquet('./history/searchHistory.parquet').select(pl.col('keys').str.split(','))
            inputData['mostSearchedKeywords']= pl.from_numpy(np.concatenate(df.collect().to_numpy().flatten())).groupby("column_0").count().sort(pl.col("count"),descending=True).to_dict()

        if 'unavailableKeys.parquet' in os.listdir('./analyticsData/') and pq.read_metadata('./analyticsData/unavailableKeys.parquet').num_rows>0:
            df= pl.scan_parquet('./analyticsData/unavailableKeys.parquet').select(pl.col('keys').str.split(','))
            inputData['unavailableKeywords']= pl.from_numpy(np.concatenate(df.collect().to_numpy().flatten())).groupby("column_0").count().sort(pl.col("count"),descending=True).to_dict()
            # print(inputData["mostSearchedKeyword"])

        if 'topResults.parquet' in os.listdir('./analyticsData/'):
            df= pl.scan_parquet('./analyticsData/topResults.parquet')
            # print("I am here")
            inputData['topDocuments']= df.groupby(["filepath","filename"]).count().sort(pl.col("count"),descending=True).collect().to_dict()
            # print("I was there")
            # print(inputData['topDocuments'])
            # print(inputData["mostSearchedKeyword"])

        if 'timeLog.parquet' in os.listdir('./analyticsData/'):
            df= pl.scan_parquet('./analyticsData/timeLog.parquet')
            inputData['timeLog']= df.collect().to_numpy().flatten()
    f.close()
    return inputData