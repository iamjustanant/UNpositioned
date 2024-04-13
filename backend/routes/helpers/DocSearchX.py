# TODO: Write the `doc_search_x_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant tweets.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from lib.Text_Processing_Utils import table
from lib.Text_Processing_Utils import smart_cosdist


def doc_search_x_handler(sql_engine,text,limit):

  if not 'x_table' in globals():
    global x_table
    x_table = table(sql_engine,'x_docs')

  query_vector = x_table.vectorizer.transform([str(text),]).toarray()

  if np.array_equal(query_vector, np.zeros(shape = query_vector.shape)):
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