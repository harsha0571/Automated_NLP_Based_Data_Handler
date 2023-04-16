

def create_keyword_index(data):

    import polars as pl
    import fastparquet as fp
    import pandas as pd
    import json
    import os
    import pyarrow.parquet as pq

    data_json = json.loads(data)

    # len_json = len(data_json)
    # print("length of json: ",len_json)

    if "doc_info.parquet" not in os.listdir("./index"):
        len_doc = 0
    else:
        len_doc = pq.read_metadata("./index/doc_info.parquet").num_rows

    # print("length of docinfo: ",len_doc)

    try:
        for i, keyword_obj in enumerate(data_json):

            key_loc = keyword_obj['doc_loc']
            key_arr = keyword_obj['keywords_array']

            for keyarr_obj in range(len(key_arr)):

                key_obj = key_arr[keyarr_obj]
                keyword_name = key_obj['keyword']
                keyword_score = key_obj['score']
                # print(i, keyword_name, keyword_score)

                if keyword_name + ".parquet" not in os.listdir("./keywords"):

                    dict = {"id": len_doc, "score": keyword_score}
                    df = pl.from_dict(data=dict, schema={
                        "id": pl.Int32, "score": pl.Float64})
                    df = df.to_pandas()
                    df.to_parquet("./keywords/" +
                                  keyword_name + ".parquet")
                else:
                    dict = {"id": len_doc, "score": keyword_score}
                    df = pl.from_dict(data=dict, schema={
                        "id": pl.Int32, "score": pl.Float64})
                    df = df.to_pandas()
                    fp.write("./keywords/"+keyword_name +
                             ".parquet", df, append=True)

            if "doc_info.parquet" not in os.listdir("./index"):
                dict = {"id": [len_doc+i], "location": [key_loc]}
                df = pl.from_dict(data=dict, schema={
                    "id": pl.Int32, "location": pl.Utf8})
                df = df.to_pandas()
                df.to_parquet("./index/doc_info.parquet")
            else:
                data = {"id": [len_doc + i], "location": [key_loc]}
                df1 = pd.DataFrame(data)
                fp.write("./index/doc_info.parquet", df1, append=True)

    except:
        print("Some error occured")
