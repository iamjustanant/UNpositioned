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
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize, TreebankWordTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')
stopwords_set = set(stopwords.words('english'))
ps = PorterStemmer()
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

def tokenize_stem_words(words:str): # CAN BE MORE EFFICIENT
    ## takes a string and converts it into a list of stemmed words

    tokens = re.findall(r'[a-z0-9]+',words.lower())
    return [ps.stem(token) for token in tokens if token not in stopwords_set]

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

    def __init__(self, sql_engine, table_name:str,df, k = 100):
        self.df = fetch_table(sql_engine,table_name)

        if os.path.isfile(table_name+'_data.pickle'):
            with open(table_name+'_data.pickle','rb') as file:
                self.svd_u, self.svd_vt = pickle.load(file)
            
        else:
            #Initialize vectorizer
            self.matrix = tfidf_vectorizer.transform(self.df['text_content'])

            self.matrix = normalize(self.matrix, axis = 1)
            
            self.svd_u,_, self.svd_vt = linalg.svds(self.matrix,k=k)
            self.svd_u = self.svd_u.astype(np.float16)
            self.svd_vt = self.svd_vt.astype(np.float16)

            with open(table_name+'_data.pickle','wb') as file:
                pickle.dump((self.svd_u, self.svd_vt), file)


        #initialize global vectorizer 
    
    def vectorize_query(query:str):
        #TODO: Put in Spellchecker
        #TODO: JUAN PUT vec2querry; str -> list[(str, weight),]
        #Only use words that are in the 
        raise NotImplementedError
        return tfidf_vectorizer.transform(query) # + take into account this weight

    def suggest_phrases(self, query:str): 
        raise NotImplementedError

        query = self.tokenize_stem_words(query)
        
    # MAIN ALGORITHM
    def svd_cossim(self, query:str, boolean_incentive = 0.5) -> np.ndarray:
        #vectorize query:
        query_vec = tfidf_vectorizer.transform([str(query),]).toarray()
        if np.array_equal(query_vec, np.zeros(shape = query_vec.shape)): 
            return None

        # Returns an array, where array[n] represents the cosine similarity of the nth document
        svd_vec = normalize(np.dot(query_vec, self.svd_vt.T)).squeeze()

        #optional boolean search weight
        boolean_search_results = self.df['text_content'].str.lower().str.contains(query).values

        return np.multiply(self.svd_u.dot(svd_vec),(boolean_search_results * boolean_incentive) + 1) #we also slightly incentivize articles with the exact (stemmed wording)


def init_tables(sql_engine):
    #Fetch from SQL Database
    global un_df, x_df, rep_df,tfidf_vectorizer, un_table,x_table,rep_table
    un_df = fetch_table(sql_engine,'un_docs')
    x_df = fetch_table(sql_engine,'x_docs')
    rep_df = fetch_table(sql_engine,'rep_docs')

    #Create Vectorizer
    if os.path.isfile('tfidf_vectorizer.pickle'): #open file if present
        with open('tfidf_vectorizer.pickle','rb') as file:
            tfidf_vectorizer = pickle.load(file)
        with open('wordlist.pickle','wb') as file:
            pickle.dump(list(tfidf_vectorizer.get_feature_names_out()), file)
    else:
        print("First-Time Initialization. This may take a minute or two...")

        tfidf_vectorizer = TfidfVectorizer(
                    min_df=0.00005,
                    max_df=0.3,
                    tokenizer=tokenize_stem_words,
                    ngram_range=(1,2)
                    )
        tfidf_vectorizer = tfidf_vectorizer.fit(pd.concat((un_df['text_content'],x_df['text_content'],rep_df['text_content'])))

    with open('tfidf_vectorizer.pickle','wb') as file:
        pickle.dump(tfidf_vectorizer, file)
    with open('wordlist.pickle','wb') as file:
        pickle.dump(list(tfidf_vectorizer.get_feature_names_out()), file)

    #Initialize tables
    #rep:0.01-0.2
    #un: 0.005
    #x
    #NOTE: these parameters are manually optimized
    un_table = table(sql_engine,'un_docs',un_df,k=100)
    x_table = table(sql_engine,'x_docs',x_df, k=200)
    rep_table = table(sql_engine,'rep_docs',rep_df, k=200)