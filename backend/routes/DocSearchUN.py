# TODO: Write the `doc_search_un_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant UN positions.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from lib.Text_Processing_Utils import table
from lib.Text_Processing_Utils import smart_cosdist


def doc_search_un_handler(sql_engine,text,limit):

  if not 'un_table' in globals():
    global un_table
    un_table = table(sql_engine,'un_docs')

  query_vector = un_table.vectorizer.transform([str(text),]).toarray()

  if np.array_equal(query_vector, np.zeros(shape = query_vector.shape)):
      return ['NO FILES FOUND',]
  else:
    results = smart_cosdist(matrix = un_table.matrix.toarray(), query_vec = query_vector)
    return un_table.df['text_content'].iloc[np.argsort(results)][:limit]