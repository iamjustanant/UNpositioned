# TODO: Write the `doc_search_un_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant UN positions.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from lib.Text_Processing_Utils import table
import pycountry

def country_map(alpha_3):
    try:
        country = pycountry.countries.get(alpha_3=alpha_3)
        return country.name
    except AttributeError:
        return 'Unknown country'

def doc_search_un_handler(sql_engine,text,limit):

  if not 'un_table' in globals():
    global un_table
    un_table = table(sql_engine,'un_docs',k=30)
    
  results = un_table.svd_cossim(text)

  if results is not None:
    """return zip(un_table.df.iloc[np.argsort(results)[::-1]][['country','year_created','text_content']][:limit].values, \
               np.sort(results)[::-1][:limit])"""
    
    # Formatted output
    ttic = [
       f"In {year}, {country_map(country).upper()} said: {tc}" 
       for country, year, tc in un_table.df.iloc[np.argsort(results)[::-1]][['country','year_created','text_content']][:limit].values
    ]

    return ttic
  
  else:
    return ['No relevant results found :(',]