# TODO: Write the `doc_search_un_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant UN positions.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import pycountry
# from lib.Utils import sparse_argsort

def country_map(alpha_3):
    try:
        country = pycountry.countries.get(alpha_3=alpha_3)
        return country.name
    except AttributeError:
        return 'Unknown country'

def doc_search_un_handler(text,limit):
  from lib.Text_Processing_Utils import un_table
  # 10-6000
    
  cossim_results = un_table.cossim(text)
  svd_results = un_table.svd_cossim(text)

  if svd_results is not None and cossim_results is not None:
    # Formatted output
    ttic = [
       f"{id}|||In {year}, {country_map(country).upper()} said: {tc}" 
       for id, country, year, tc in un_table.df[['id','country','year_created','text_content']].iloc[np.lexsort((svd_results,cossim_results))][::-1][:limit].values
    ]
    return ttic
  
  else:
    return ['No relevant results found :(',]