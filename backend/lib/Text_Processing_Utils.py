import numpy as np
import pandas as pd
import re
import os
import pickle

from scipy.sparse import linalg, csc_matrix

from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk

# one-time downloads
# nltk.download('stopwords')
# nltk.download('punkt')

from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

stopwords_set = set(stopwords.words('english'))
ps = PorterStemmer()

import pycountry

countries = list(pycountry.countries)
country_alpha3_list = [country.alpha_3 for country in countries]

def country_map(alpha_3):
    try:
        country = pycountry.countries.get(alpha_3=alpha_3)
        return country.name.upper()
    except AttributeError:
        return 'Unknown country'


def fetch_table(sql_engine, table_name:str):
    """
    fetch table from SQL and process certain UN docs
    """
    data = sql_engine.query_selector("SELECT * FROM " + table_name)
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()

    if table_name == 'un_docs':
        # REMOVE UNKNOWN COUNTRIES
        df = df[df['country'].isin(country_alpha3_list)]
        # Full country names
        df['country'] = df['country'].apply(country_map)

        #exploding by sentence
        df['text_content'] = df['text_content'].apply(sent_tokenize)
        df = df.explode('text_content').reset_index(names='paragraph_index')
        
        # clean 
        df = df[df['text_content'].str.len() >= 30]

    elif table_name == 'x_docs':
        # remove dupes
        df['dup'] = df['text_content'].apply(lambda x: x.split(' https')[0])
        df = df.drop_duplicates(subset=['dup'])
        df = df.drop('dup', axis=1)

        # remove excessively long documents
        df = df[df['text_content'].str.len() < 600]

        # remove non-ascii characters
        df['user_name'] = df['user_name'].apply(lambda string: re.sub(r"\b([^\s]+)\\([^\s]+)\b",r'\1', \
                                                                        str(string.encode('ascii', 'ignore'), 'ascii')))
    else:   # rep_docs
        # remove excessively long documents
        df = df[df['text_content'].str.len() < 600]

        # single quotes
        df['author'] = df['author'].str.replace('&#x27;', "'")
    
    
    # more cleaning
    df['text_content'] = df['text_content'].str.replace(r'\s+', ' ', regex=True) # remove spaces

    # remove nextlines
    df['text_content'] = df['text_content'].str.replace('\n',' ') 
    df['text_content'] = df['text_content'].str.replace('\x0c',' ')
    
    # remove non-ascii characters
    df['text_content'] = df['text_content'].apply(lambda string: re.sub(r"\b([^\s]+)\\([^\s]+)\b",r'\1', \
                                                                        str(string.encode('ascii', 'ignore'), 'ascii')))
    
    # fix amperstands
    df['text_content'] = df['text_content'].str.replace('&amp;','&')

    # reset index
    df = df.drop('id', axis=1)
    df = df.reset_index(drop=True)
    df['id'] = df.index

    return df


def tokenize_stem_words(words:str): # CAN BE MORE EFFICIENT (?)
    """
    takes a string and converts it into a list of stemmed words
    """
    tokens = re.findall(r'[a-z0-9]+',words)
    return [ps.stem(token) for token in tokens if token not in stopwords_set]

class table:
    # NOTE: you should pass your own value for `min_df` and `max_df`
    #see https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html

    def __init__(self, sql_engine, table_name:str,df, k = 100):

        def open_pickle_if_present(filename:str):
            if os.path.isfile('lib/' + self.table_name + '_' + filename + '.pickle'):
                with open('lib/' + self.table_name + '_' + filename + '.pickle','rb') as file:
                    data = pickle.load(file)
                return data
            else:
                return None
            
        self.df = df
        self.table_name = table_name

        #Load files if present
        self.svd_u = open_pickle_if_present('u')
        self.svd_s = open_pickle_if_present('s')
        self.svd_vt = open_pickle_if_present('vt')
        self.matrix = open_pickle_if_present('matrix')

        if self.svd_u is None or self.svd_s is None or self.svd_vt is None or self.matrix is None:  #if any file is absent
            #Initialize tfidf matrix
            print("Initializing Matrices...")
            self.matrix = tfidf_vectorizer.transform(self.df['text_content'])
            # self.matrix = normalize(self.matrix, axis = 1)
            with open('lib/'+table_name+'_matrix.pickle','wb') as file:
                pickle.dump(self.matrix,file)

            #Create and save svd matrices
            self.svd_u,self.svd_s, self.svd_vt = linalg.svds(self.matrix,k=k)
            self.svd_u = self.svd_u.astype(np.float16)
            self.svd_vt = self.svd_vt.astype(np.float16)
            self.svd_s = self.svd_s.astype(np.float16)

            with open('lib/'+table_name+'_u.pickle','wb') as file:
                pickle.dump(self.svd_u,file)
            with open('lib/'+table_name+'_s.pickle','wb') as file:
                pickle.dump(self.svd_s,file)
            with open('lib/'+table_name+'_vt.pickle','wb') as file:
                pickle.dump(self.svd_vt,file)

    def cossim(self,query:str) -> np.ndarray:
        # Returns an array, where array[n] represents the cosine similarity of the nth document
        query_vec = tfidf_vectorizer.transform([str(query),]).toarray()
        matrix = csc_matrix(self.matrix)

        assert matrix.shape[1] == query_vec.shape[1]
        query_vec = query_vec.flatten()

        relevant_terms = np.nonzero(query_vec)[0]

        query_vec = query_vec[relevant_terms]
        matrix = matrix[:,relevant_terms]
        
        if np.sum(query_vec) == 0 and np.sum(matrix) == 0: #matrix is empty
            return None
        else:
            return cosine_similarity(matrix,query_vec.reshape(1,-1)).flatten()

    def svd_cossim(self, query:str, boolean_incentive = 1) -> np.ndarray:
        #vectorize query:
        query_vec = tfidf_vectorizer.transform([str(query),]).toarray()
        if np.array_equal(query_vec, np.zeros(shape = query_vec.shape)): 
            return None

        # Returns an array, where array[n] represents the cosine similarity of the nth document
        svd_vec = normalize(np.dot(query_vec, self.svd_vt.T)).squeeze()

        #optional boolean search weight
        boolean_search_results = self.df['text_content'].str.lower().str.contains(query).values

        #we also slightly incentivize articles with the exact (stemmed wording)
        return np.multiply(self.svd_u.dot(svd_vec),(boolean_search_results * boolean_incentive) + 1)
    

def init_tables(sql_engine):
    #Fetch from SQL Database
    global un_df, x_df, rep_df,tfidf_vectorizer, un_table,x_table,rep_table
    un_df = fetch_table(sql_engine,'un_docs')
    x_df = fetch_table(sql_engine,'x_docs')
    rep_df = fetch_table(sql_engine,'rep_docs')

    #Create Vectorizer
    if os.path.isfile('lib/tfidf_vectorizer.pickle'): #open file if present
        with open('lib/tfidf_vectorizer.pickle','rb') as file:
            tfidf_vectorizer = pickle.load(file)
    else:
        print("First-Time Initialization. This may take a minute or two...")

        tfidf_vectorizer = TfidfVectorizer(
                    min_df=0.0001,
                    max_df=0.3,
                    tokenizer=tokenize_stem_words,
                    ngram_range=(1,2)
                    )
        tfidf_vectorizer = tfidf_vectorizer.fit(pd.concat((un_df['text_content'],x_df['text_content'],rep_df['text_content'])))

        with open('lib/tfidf_vectorizer.pickle','wb') as file:
            pickle.dump(tfidf_vectorizer, file)

    #Initialize tables
    #original min_df: 0.00005
    #NOTE: these parameters are manually optimized
    un_table = table(sql_engine,'un_docs',un_df,k=30)
    x_table = table(sql_engine,'x_docs',x_df, k=30)
    rep_table = table(sql_engine,'rep_docs',rep_df, k=30)