import numpy as np
import pandas as pd
import re
import json
import os
import pickle

# Objectives for search:
# Search entire phrases smartly
# Faster search

from sklearn.preprocessing import normalize
from scipy.sparse import linalg, csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


import nltk
nltk.download('stopwords')
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize, TreebankWordTokenizer
from nltk.corpus import stopwords
from scipy.spatial import distance

def fetch_table(sql_engine, table_name:str): #fetch table from SQL and process certain UN docs
    data = sql_engine.query_selector("SELECT * FROM " + table_name)
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()

    if table_name == 'un_docs':
        #exploding by sentence
        df['text_content'] = df['text_content'].apply(sent_tokenize)
        df = df.explode('text_content').reset_index(names='paragraph_index')

        #cleaning
        df = df[df['text_content'].str.len() >= 30]
        df['text_content'] = df['text_content'].str.replace('\s{2,}',' ',regex=True) #delete duplicate spaces
        df['text_content'] = df['text_content'].str.replace('\n',' ') #Removing nextlines
        df['text_content'] = df['text_content'].str.replace('\x0c',' ')

        df = df[df['text_content'].str.len() >= 5]

        df['text_content'] = df['text_content'].astype('str')

        df['sess'] = df['sess'].astype('int')
        df['year_created'] = df['year_created'].astype('int')
        df['country'] = df['country'].astype('str')
        df = df[df['year_created'] >= 2000]
    return df

# old cossim
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

class table:
    # NOTE: you should pass your own value for `min_df` and `max_df`
    #see https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html

    def __init__(self, sql_engine, table_name:str,min_df:float=100,max_df:float=10000, k = 100):
        self.stopwords_set = set(stopwords.words('english'))
        self.ps = PorterStemmer()
        self.tokenizer = TreebankWordTokenizer()

        if os.path.isfile(table_name+'_data.pickle'):
            with open(table_name+'_data.pickle','rb') as file:
                self.vectorizer, self.matrix,self.svd_u, self.svd_s, self.svd_vt = pickle.load(file)
            self.df = fetch_table(sql_engine,table_name)   
        else:
            self.df = fetch_table(sql_engine,table_name)
            self.vectorizer = TfidfVectorizer(
            min_df=min_df,
            max_df=max_df,
            tokenizer=self.tokenize_stem_words,
            ngram_range=(1,2)
            )
            self.vectorizer = self.vectorizer.fit(self.df['text_content'])

            self.matrix = self.vectorizer.transform(self.df['text_content'])

            self.matrix = normalize(self.matrix, axis = 1)
            
            self.svd_u, self.svd_s, self.svd_vt = linalg.svds(self.matrix,k=k)

            with open(table_name+'_data.pickle','wb') as file:
                pickle.dump((self.vectorizer, self.matrix, self.svd_u, self.svd_s, self.svd_vt), file)
    
    def vectorize_query(query:str):
        #TODO: Put in Spellchecker
        #TODO: JUAN PUT vec2querry; str -> list[(str, weight),]
        #Only use words that are in the 
        raise NotImplementedError
        return self.vectorizer.transform(query) # + take into account this weight

    def suggest_phrases(self, query:str): 
        raise NotImplementedError

        query = self.tokenize_stem_words(query)
        
    def tokenize_stem_words(self,words:str): # CAN BE MORE EFFICIENT
        ## takes a string and converts it into a list of stemmed words

        tokens = re.findall(r'[a-z0-9]+',words.lower())
        return [self.ps.stem(token) for token in tokens if token not in self.stopwords_set]
    
    # MAIN ALGORITHM
    def svd_cossim(self, query:str, boolean_incentive = 0.5) -> np.ndarray:
        #vectorize query:
        query_vec = self.vectorizer.transform([str(query),]).toarray()
        if np.array_equal(query_vec, np.zeros(shape = query_vec.shape)): 
            return None

        # Returns an array, where array[n] represents the cosine similarity of the nth document
        svd_vec = normalize(np.dot(query_vec, self.svd_vt.T)).squeeze()

        #optional boolean search weight
        boolean_search_results = self.df['text_content'].str.lower().str.contains(query).values

        return np.multiply(self.svd_u.dot(svd_vec),(boolean_search_results * boolean_incentive) + 1) #we also slightly incentivize articles with the exact (stemmed wording)