import numpy as np
import pandas as pd
import re
import json
import os

# Objectives for search:
# Search entire phrases smartly
# Faster search

from sklearn.preprocessing import normalize
from scipy.sparse import linalg
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
"""
def smart_cosdist(matrix:np.ndarray,query_vec:np.ndarray) -> np.ndarray:
    # Returns an array, where array[n] represents the cosine similarity of the nth document

    assert matrix.shape[1] == query_vec.shape[1]
    query_vec = query_vec.flatten()

    relevant_terms = np.nonzero(query_vec)[0]

    query_vec = query_vec[relevant_terms]
    matrix = matrix[:,relevant_terms]

    return np.array([distance.cosine(matrix[doc_index],query_vec) 
                     if not np.all(matrix[doc_index,:] == 0) else np.inf 
                     for doc_index in range(0,matrix.shape[0])])
"""
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
        max_df=max_df,
        tokenizer=self.tokenize_stem_words
        )
        self.vectorizer = self.vectorizer.fit(self.df['text_content'])

        self.matrix = self.vectorizer.transform(self.df['text_content'])
        self.matrix = normalize(self.matrix, axis = 1)


    def phrase_tokenizer(self, words:str):
        token_corr = np.corrcoef(self.matrix,rowvar=False)

        tokens = re.findall(r"[a-z]{2,}",words.lower())
        #tokens = [self.ps.stem(token) for token in tokens if token not in self.stopwords_set]
        phrase_tokens = []
        index = 0
        while index < len(tokens):
            if tokens[index] not in self.stopwords_set:
                tokens[index] = self.ps.stem(tokens[index])
                if token_corr[self.ps.stem(tokens[index + 1]),self.ps.stem(tokens[index])] > 0.7:
                    phrase_tokens[index] = tokens[index] + " " + tokens[index + 1]
                else:
                    phrase_tokens[index] = tokens[index]
                    index += 1
        return phrase_tokens
                    
    def suggest_phrases(self, query:str):
        query_vec = self.vectorizer.transform([str(query),]).toarray()
        if np.array_equal(query_vec, np.zeros(shape = query_vec.shape)): 
            return None
        
        self.count_vectorizor = CountVectorizer(min_df=10, tokenizer = self.phrase_tokenizer)

        
    def tokenize_stem_words(self,words:str): # CAN BE MORE EFFICIENT
        ## takes a string and converts it into a list of stemmed words
        tokens = re.findall(r"[a-z]{2,}",words.lower())
        return [self.ps.stem(token) for token in tokens if token not in self.stopwords_set]        
    
    def svd_cossim(self, query:str,k=20, boolean_incentive = 0.2) -> np.ndarray:
        #vectorize query:
        query_vec = self.vectorizer.transform([str(query),]).toarray()
        if np.array_equal(query_vec, np.zeros(shape = query_vec.shape)): 
            return None

        #initialize svd matrix if needed
        if not all(hasattr(self, attribute) for attribute in ['svd_u','svd_s','svd_vt']):
            self.svd_u, self.svd_s, self.svd_vt = linalg.svds(self.matrix,k=k)

        # Returns an array, where array[n] represents the cosine similarity of the nth document
        svd_vec = normalize(np.dot(query_vec, self.svd_vt.T)).squeeze()

        #optional boolean search weight
        boolean_search_results = self.df['text_content'].str.contains(query).values

        return np.multiply(self.svd_u.dot(svd_vec),(boolean_search_results * boolean_incentive) + 1) #we also slightly incentivize articles with the exact (stemmed wording)