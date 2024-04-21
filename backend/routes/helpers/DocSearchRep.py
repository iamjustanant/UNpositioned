# TODO: Write the `doc_search_un_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant UN positions.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from lib.Utils import sparse_argsort

def doc_search_rep_handler(sql_engine,text,limit):
  from lib.Text_Processing_Utils import rep_table
  results = rep_table.svd_cossim(text)

  if results is not None:
    """return zip(un_table.df.iloc[np.argsort(results)[::-1]][['country','year_created','text_content']][:limit].values, \
               np.sort(results)[::-1][:limit])"""
    
    # Formatted output
    ttic = [
       f"{author} said on {ms.upper()}: {tc}" 
       for ms, author, tc in rep_table.df[['media_source','author','text_content']].iloc[sparse_argsort(results)][::-1][:limit].values
    ]

    return ttic
  
  else:
    return ['No relevant results found :(',]

  if np.array_equal(query_vector, np.zeros(shape = query_vector.shape)):
      return ['No relevant results found :(',]
  else:
    results = smart_cosdist(matrix = rep_table.matrix.toarray(), query_vec = query_vector)
    # return rep_table.df['text_content'].iloc[np.argsort(results)][:limit]

    # Formatted output
    ttic = [
       f"{author} said on {ms.upper()}: {tc}" 
       for ms, author, tc in rep_table.df[['media_source','author','text_content']].iloc[np.argsort(results)][:limit].values
    ]

    return ttic
  
