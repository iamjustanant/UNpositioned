# TODO: Write the `doc_search_x_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant tweets.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

# from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
# from lib.Utils import sparse_argsort




def doc_search_x_handler(text,limit):
  from lib.Text_Processing_Utils import x_table

  cossim_results = x_table.cossim(text)
  svd_results = x_table.svd_cossim(text)

  if cossim_results is not None and svd_results is not None:
    
    # Formatted output
    ttic = [
      # ID, Followers, Verified, User Name, Text Content
      f"{id}||| {int(flw)} ||| {bool(ver)} ||| {user} said: {tc}" 
       for id, flw, ver, user, tc in x_table.df[['id', 'followers', 'verified', 
                                                 'user_name', 'text_content']].iloc
                                                 [np.lexsort((svd_results,cossim_results))][::-1][:limit].values
    ]
    return ttic
  
  else:
    return ['No relevant results found :(',]
  