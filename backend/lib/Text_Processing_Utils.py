import numpy as np
import pandas as pd
import re
import json
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import nltk
nltk.download('stopwords')

from nltk.stem.porter import *
from nltk.corpus import stopwords
from scipy.spatial import distance

def fetch_table(sql_engine, table_name:str):
    data = sql_engine.query_selector("SELECT * FROM " + table_name)
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()
    return df

def smart_cosdist(matrix:np.ndarray,query_vec:np.ndarray) -> np.ndarray:
    # Returns an array, where array[n] represents the cosine similarity of the nth document

    assert matrix.shape[1] == query_vec.shape[1]
    query_vec = query_vec.flatten()

    relevant_terms = np.nonzero(query_vec)[0]

    query_vec = query_vec[relevant_terms]
    matrix = matrix[:,relevant_terms]

    return np.array([distance.cosine(matrix[doc_index],query_vec) if not np.all(matrix[doc_index,:] == 0) else np.inf for doc_index in range(0,matrix.shape[0])])

class table:
    # NOTE: you should pass your own value for `min_df` and `max_df`
    #see https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html
    def __init__(self, sql_engine, table_name:str,min_df:float=0.0001,max_df:float=0.99):
        self.df = fetch_table(sql_engine,table_name)

        self.ps = PorterStemmer()

        #stem and tokenize
        self.stopwords_set = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(
        min_df=min_df,
        max_df=max_df
        #tokenizer=self.tokenize_stem_words
        )
        self.vectorizer = self.vectorizer.fit(self.df['text_content'])


        self.matrix = self.vectorizer.transform(self.df['text_content'])

    def tokenize_stem_words(self,words:str) -> str: # CAN BE MORE EFFICIENT
        ## takes a string and converts it into a list of stemmed words
        tokens = re.findall(r"[a-z]{2,}",words.lower())
        return [self.ps.stem(token) for token in tokens if token not in self.stopwords_set]