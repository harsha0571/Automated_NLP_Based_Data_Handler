# importing libraries for searching operation
import polars as pl                             # used to open index files and perform search for docid
import time                                     # used to calcuate time taken for each operation
# import vaex                                     # used for mapping to locations stored in hdf5 file
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
    biasFiles= [keys + 'Bias' + extension for keys in keywordList]
    globalBiasPath= [directory + file for file in biasFiles]

    # accessing the document-location file stored in hdf5 format
    # locationData= vaex.open(directory + 'addressBook.hdf5')     # memory mapping for faster access

    total_rows= 0                       # total number of rows considering all keyword index files
    maxRowNo= 50000000                 # the last document to be added in the file system
    
    # finding the total rows to be read for all index files respective to keywords
    for i in globalIndexPath:           
        total_rows+= pq.read_metadata(i).num_rows
        print(total_rows)
    
    # performing full scale reading of all index files at once if total rows less than the threshold
    if total_rows <= 30000000:
        indexList= [i for i in range(len(keywordList))]             # list for storing index data for each keyword
        biasList= [i for i in range(len(keywordList))]
        for i in range(len(globalIndexPath)):
            
            indexList[i]= pl.scan_parquet(
                                        source= globalIndexPath[i],
                                        parallel= 'auto',
                                        low_memory=True
                                    )
            biasList[i]=  pl.scan_parquet(
                                        source= globalBiasPath[i],
                                        parallel= 'auto',
                                        low_memory=True
                                   )
        concatDf= pl.concat(indexList)                      #combining all keywords' index info
        biasDf= pl.concat(biasList)

        # add the 'bias' column to the index dataframe
        concatDf= concatDf.with_columns(pl.lit(biasDf.select('bias').collect().to_series()).alias('bias'))
        # performing the multiplication of bias and score
        concatDf= concatDf.with_columns( (pl.col('score') * pl.col('bias')).alias('score') )
        concatDf.drop('bias')
        result= concatDf.groupby('id').agg([pl.sum('score'), pl.count()]).sort(by='score',descending=True)[:100]
    
    else:
        rangeSize= 40000000
        lLimit= 1
        uLimit= rangeSize
        counter=0
        resultList= [i for i in range(int(math.ceil(maxRowNo/float(rangeSize))))]
        while lLimit<= maxRowNo:
            indexList= [i for i in range(len(keywordList))]
            biasList= [i for i in range(len(keywordList))]
        
            for i in range(len(globalIndexPath)):
                indexList[i]= pl.scan_parquet(
                                        source= globalIndexPath[i],
                                        parallel= 'auto',
                                        low_memory=True
                                    ).filter((pl.col('id')>=lLimit) & (pl.col('id')<uLimit))
                biasList[i]=  pl.scan_parquet(
                                        source= globalBiasPath[i],
                                        parallel= 'auto',
                                        low_memory=True
                                    ).filter((pl.col('id')>=lLimit) & (pl.col('id')<uLimit))
            concatDf= pl.concat(indexList)
            biasDf= pl.concat(biasList)
            concatDf= concatDf.with_columns(pl.lit(biasDf.select('bias').collect().to_series()).alias('bias'))
            concatDf= concatDf.with_columns( (pl.col('score') * pl.col('bias')).alias('score') )
            resultList[counter]= concatDf.groupby('id').agg([pl.sum('score'), pl.count()]).sort(by='score',descending=True)[:100]
            counter+=1
            lLimit= uLimit
            uLimit+=rangeSize
        result= pl.concat(resultList).sort('score', descending= True)[:100]

    return result.collect()
    # idArray= result.collect().drop('score').to_numpy()
    # return locationData[locationData['id'].isin(idArray)]

start= time.time()
print(searchForDocuments('D:/aditya/Final Year/Project Work/Automated_NLP_Based_Data_Handler/personalTests/vaex/data/medium',
                     ['newSample1','newSample2','newSample3','newSample4','newSample5','newSample6','newSample7','newSample8','newSample9','newSample10','newSample11','newSample12']))
stop= time.time()
print('Total time:',stop-start,"sec")