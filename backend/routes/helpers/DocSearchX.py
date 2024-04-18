# TODO: Write the `doc_search_x_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant tweets.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from lib.Text_Processing_Utils import smart_cosdist


def doc_search_x_handler(sql_engine,text,limit):
  from lib.Text_Processing_Utils import x_table
  results = x_table.svd_cossim(text)

  if results is not None:
    """return zip(un_table.df.iloc[np.argsort(results)[::-1]][['country','year_created','text_content']][:limit].values, \
               np.sort(results)[::-1][:limit])"""
    
    # Formatted output
    ttic = [
      f"{user} said: {tc}" 
       for user, tc in x_table.df[['user_name', 'text_content']].iloc[np.argsort(results)][::-1][:limit].values
    ]

    return ttic
  
  else:
    return ['No relevant results found :(',]

  if np.sum(query_vector) == 0:
      return ['No relevant results found :(',]
  else:
    results = smart_cosdist(matrix = x_table.matrix.toarray(), query_vec = query_vector)
    # return x_table.df['text_content'].iloc[np.argsort(results)][:limit]

    # Formatted output
    ttic = [
       f"{user} said: {tc}" 
       for user, tc in x_table.df[['user_name', 'text_content']].iloc[np.argsort(results)][:limit].values
    ]

    return ttic
  