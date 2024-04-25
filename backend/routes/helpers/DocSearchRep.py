# TODO: Write the `doc_search_un_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant UN positions.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
# from lib.Utils import sparse_argsort

def doc_search_rep_handler(text,limit):
  from lib.Text_Processing_Utils import rep_table

  cossim_results = rep_table.cossim(text)
  svd_results = rep_table.svd_cossim(text)

  if cossim_results is not None or svd_results is not None:
    
    # Formatted output
    ttic = [
       f"{id-1}|||{author} said on {ms.upper()}: {tc}" 
       for id, ms, author, tc in rep_table.df[['id','media_source','author','text_content']].iloc[
         np.lexsort((svd_results,cossim_results))][::-1][:limit].values
    ]
    return ttic
  
  else:
    return ['No relevant results found :(',]
