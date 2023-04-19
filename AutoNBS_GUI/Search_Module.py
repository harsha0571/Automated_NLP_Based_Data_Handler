import polars as pl
import os
searchHistLoc = './history/'
histFilePath = searchHistLoc+'searchHistory.parquet'


def searchForDocuments(directoryPath, keywordList):

    import pyarrow.parquet as pq
    import math

    keyBias = {}
    # to find if search history bias is usable or not
    if 'searchHistory.parquet' in os.listdir(searchHistLoc):
        totalSearches = pq.read_metadata(histFilePath).num_rows
        if totalSearches > 100:
            df = pl.read_parquet(histFilePath)
            for key in keywordList:
                keyBias[key] = 10 + \
                    (len(df.filter(pl.col('keys').str.contains(key)))/totalSearches)
            del df

    # assembling the global path for each index and bias files of parquet format
    directory = directoryPath + '/'
    extension = '.parquet'
    indexFiles = [keys + extension for keys in keywordList]
    globalIndexPath = [directory + file for file in indexFiles]

    # To access the id-location file
    # addressBook= pl.scan_parquet('./datasets/doc_info.parquet)
    # lastId= pq.read_metadata('./datasets/doc_info.parquet').num_rows      # finds the total no. of docs in system
    lastId = 50000000

    # total number of rows considering all keyword index files
    total_rows = 0
    maxRowNo = 50000000                 # the last document to be added in the file system
    # list of total number documents containing each keyword
    rowLenghtList = [i for i in range(len(keywordList))]

    # finding the total rows to be read for all index files respective to keywords
    for index, i in enumerate(globalIndexPath):
        rowLenghtList[index] = pq.read_metadata(i).num_rows
        total_rows += rowLenghtList[index]

    # performing full scale reading of all index files at once if total rows less than the threshold
    if total_rows <= 30000000:
        # list for storing index data for each keyword
        indexList = [i for i in range(len(keywordList))]

        for i in range(len(globalIndexPath)):

            indexList[i] = pl.scan_parquet(
                source=globalIndexPath[i],
                parallel='auto',
                low_memory=True
            )

            # updating the score by taking its product with idf value of each keyword
            indexList[i] = indexList[i].with_columns(
                (pl.col('score') * math.log10(lastId/float(rowLenghtList[i]))).alias('score'))
            if keywordList[i] in keyBias:
                indexList[i] = indexList[i].with_columns(
                    (pl.col('score') * keyBias[keywordList[i]]).alias('score'))

        concatDf = pl.concat(indexList)  # combining all keywords' index info
        result = concatDf.groupby('id').agg([pl.mean('score'), pl.count()]).sort(
            by='score', descending=True)[:100]

    else:
        # to access documents with id in the range of 'n' 40000000
        rangeSize = 40000000
        lLimit = 1                               # lowest id value for each range
        uLimit = rangeSize                       # highes id value for each range
        # to track the result of each iteration of ranges
        counter = 0

        # total number of iterations required to read through all index files completely
        resultList = [i for i in range(
            int(math.ceil(maxRowNo/float(rangeSize))))]

        # iteration with the condition that the lower id should never exceed the id of the last document in system
        while lLimit <= maxRowNo:
            indexList = [i for i in range(len(keywordList))]

            # to read through each keyword index files withing a specified range
            for i in range(len(globalIndexPath)):

                indexList[i] = pl.scan_parquet(
                    source=globalIndexPath[i],
                    parallel='auto',
                    low_memory=True
                ).filter((pl.col('id') >= lLimit) & (pl.col('id') < uLimit))
                # to update the score of each ranged data of the keyword using its 'idf' value
                indexList[i] = indexList[i].with_columns(
                    (pl.col('score')*math.log10(lastId/float(rowLenghtList[i]))).alias('score'))
                if keywordList[i] in keyBias:
                    indexList[i] = indexList[i].with_columns(
                        (pl.col('score') * keyBias[keywordList[i]]).alias('score'))
            # to vertically merge the ranged info read from each keyword
            concatDf = pl.concat(indexList)

            # Performing grouping, aggregation and slicing for getting the top 100 results based on score
            resultList[counter] = concatDf.groupby('id').agg(
                [pl.mean('score'), pl.count()]).sort(by='score', descending=True)[:100]

            # updating iteration specific variables
            counter += 1
            lLimit = uLimit
            uLimit += rangeSize

        # vertically merging the results of each ranged details
        result = pl.concat(resultList).sort('score', descending=True)[:100]

    # updateSearchHistory(keywordList)
    result = result.select('id').collect().to_series()
    # return result.collect()             # to execute the lazy dataframe of the polars library

    # to return the location of the top 100 files
    pathFinder = pl.scan_parquet('./index/doc_info.parquet')
    pathFinder = pathFinder.filter(
        pl.col('id').is_in(result)).select('location')
    res = pathFinder.collect()
    return res


def updateSearchHistory(keyList, keysNotFound, topResults, timeTaken):
    if 'searchHistory.parquet' not in os.listdir(searchHistLoc):
        data = {'keys': [','.join(keyList)]}
        pl.from_dict(data).write_parquet(histFilePath)
    else:
        df = pl.scan_parquet(histFilePath)

        df = df.collect().extend(pl.from_dict({'keys': [','.join(keyList)]}))
        if len(df) > 10000:
            df = df[1:]

        df.write_parquet(histFilePath)
    if 'unavailableKeys.parquet' not in os.listdir('./analyticsData/'):
        dat= {'keys': [','.join(keysNotFound)]}
        pl.from_dict(dat).write_parquet('./analyticsData/unavailableKeys.parquet')
    else:
        df1= pl.scan_parquet('./analyticsData/unavailableKeys.parquet')
        df1= df1.collect().extend(pl.from_dict({'keys': [','.join(keysNotFound)]}))
        if len(df1)>10000:
            df1= df1[1:]
        df1.write_parquet("./analyticsData/unavailableKeys.parquet")

    topData= {'filename': [result[0] for result in topResults], 'filepath': [result[1] for result in topResults]}
    if 'topResults.parquet' not in os.listdir('./analyticsData/'):
        pl.from_dict(topData).write_parquet('./analyticsData/topResults.parquet')
    else:
        df2= pl.scan_parquet('./analyticsData/topResults.parquet')
        df2= df2.collect().extend(pl.from_dict(topData))
        if len(df2)>100000:
            extraRows= len(df2)- 100000
            df2= df2[extraRows:]
        df2.write_parquet("./analyticsData/topResults.parquet")

    timeData= {"timeElapsed": [timeTaken]}
    if 'timeLog.parquet' not in os.listdir('./analyticsData'):
        pl.from_dict(timeData).write_parquet('./analyticsData/timeLog.parquet')
    else:
        df3= pl.scan_parquet('./analyticsData/timeLog.parquet')
        df3= df3.collect().extend(pl.from_dict(timeData))
        if len(df3)>10000:
            df3= df3[1:]
        df3.write_parquet('./analyticsData/timeLog.parquet')
