# importing libraries for searching operation
import polars as pl                             # used to open index files and perform search for docid
import time                                     # used to calcuate time taken for each operation
import pyarrow.parquet as pq                    # used internally by polars
import math

# directoryPath:- location of directory containing the index files
# keywordList:- list of keywords which will be the name of each index files along with bias files
# return a list of filepaths based on final score in descending order
def searchForDocuments(directoryPath, keywordList):
    
    # assembling the global path for each index and bias files of parquet format
    directory= directoryPath + '/'
    extension= '.parquet'
    indexFiles= [keys + 'Index' + extension for keys in keywordList]
    globalIndexPath= [directory + file for file in indexFiles]

    # To access the id-location file
    # addressBook= pl.scan_parquet('./datasets/doc_info.parquet)
    # lastId= pq.read_metadata('./datasets/doc_info.parquet').num_rows      # finds the total no. of docs in system
    lastId= 50000000

    total_rows= 0                       # total number of rows considering all keyword index files
    maxRowNo= 50000000                 # the last document to be added in the file system
    rowLenghtList= [i for i in range(len(keywordList))]     # list of total number documents containing each keyword

    # finding the total rows to be read for all index files respective to keywords
    for index,i in enumerate(globalIndexPath):      
        rowLenghtList[index]= pq.read_metadata(i).num_rows
        total_rows+= rowLenghtList[index]
        print(total_rows)
    
    # performing full scale reading of all index files at once if total rows less than the threshold
    if total_rows <= 30000000:
        indexList= [i for i in range(len(keywordList))]             # list for storing index data for each keyword
        
        for i in range(len(globalIndexPath)):
            indexList[i]= pl.scan_parquet(
                                        source= globalIndexPath[i],
                                        parallel= 'auto',
                                        low_memory=True
                                    )
            # updating the score by taking its product with idf value of each keyword
            indexList[i]= indexList[i].with_columns((pl.col('score')* math.log10(lastId/float(rowLenghtList[i]))).alias('score'))
        
        concatDf= pl.concat(indexList)                      #combining all keywords' index info
        result= concatDf.groupby('id').agg([pl.sum('score'), pl.count()]).sort(by='score',descending=True)[:100]
    
    else:
        rangeSize= 40000000                     # to access documents with id in the range of 'n' 40000000 
        lLimit= 1                               # lowest id value for each range
        uLimit= rangeSize                       # highes id value for each range
        counter= 0                              # to track the result of each iteration of ranges

        # total number of iterations required to read through all index files completely
        resultList= [i for i in range(int(math.ceil(maxRowNo/float(rangeSize))))]

        #iteration with the condition that the lower id should never exceed the id of the last document in system
        while lLimit<= maxRowNo:
            indexList= [i for i in range(len(keywordList))]

            # to read through each keyword index files withing a specified range
            for i in range(len(globalIndexPath)):
                indexList[i]= pl.scan_parquet(
                                        source= globalIndexPath[i],
                                        parallel= 'auto',
                                        low_memory=True
                                    ).filter((pl.col('id')>=lLimit) & (pl.col('id')<uLimit))
                # to update the score of each ranged data of the keyword using its 'idf' value
                indexList[i]= indexList[i].with_columns((pl.col('score')*math.log10(lastId/float(rowLenghtList[i]))).alias('score'))
               
            concatDf= pl.concat(indexList)      # to vertically merge the ranged info read from each keyword
            
            # Performing grouping, aggregation and slicing for getting the top 100 results based on score
            resultList[counter]= concatDf.groupby('id').agg([pl.sum('score'), pl.count()]).sort(by='score',descending=True)[:100]

            # updating iteration specific variables
            counter+=1
            lLimit= uLimit
            uLimit+=rangeSize
        
        # vertically merging the results of each ranged details
        result= pl.concat(resultList).sort('score', descending= True)[:100]

    # result= result.select('id')
    return result.collect()             # to execute the lazy dataframe of the polars library
    
    # to return the location of the top 100 files
    # pathFinder= pl.scan_parquet('./datasets/doc_info.parquet')
    # pathFinder= pathFinder.filter(pl.col('id').is_in(result)).select('location')
    # return pathFinder.collect()

start= time.time()
# path= './datasets/'
# searchForDocuments(path, keyWordList)
print(searchForDocuments('D:/aditya/Final Year/Project Work/Automated_NLP_Based_Data_Handler/personalTests/vaex/data/small',
                     ['newSample1','newSample2','newSample3','newSample4','newSample5','newSample6','newSample7','newSample8','newSample9','newSample10']))
stop= time.time()
print('Total time:',stop-start,"sec")