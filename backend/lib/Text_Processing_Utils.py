import numpy as np
import pandas as pd
import re
import json
import os
import pickle

# Objectives for search:
# Search entire phrases smartly
# Faster search

from scipy.spatial import distance
from scipy.sparse import linalg, csc_matrix, csr_matrix

from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.neighbors import NearestNeighbors

from collections import defaultdict

import nltk

# one-time downloads
nltk.download('stopwords')
nltk.download('punkt')

from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize, TreebankWordTokenizer, word_tokenize
from nltk.corpus import stopwords

# Spellchecker
from spellchecker import SpellChecker

stopwords_set = set(stopwords.words('english'))
ps = PorterStemmer()

spell = SpellChecker()
spell.word_frequency.load_dictionary('lib/en.json')

# loading the dictionary filled with similarity scores for words in the query
with open('lib/pickle_dict','rb') as file:
    pickled_dict = pickle.load(file)


def invert_nested_dict(nested_dictionary):
    """
    inverts the indexes of a nested dictionary, using the keys from the nested dictionary
    as the new keys, and puts the inverted values in a
    """
    inv_pickled_dict = defaultdict(list)  
    for outer_key, inner_dict in nested_dictionary.items():
        for inner_key in inner_dict.keys():
            inv_pickled_dict[inner_key].append(outer_key)  
    return dict(inv_pickled_dict)  

inv_pickled_dict = invert_nested_dict(pickled_dict)

def fetch_table(sql_engine, table_name:str):
    """
    fetch table from SQL and process certain UN docs
    """
    data = sql_engine.query_selector("SELECT * FROM " + table_name)
    df = pd.DataFrame(data.fetchall())
    df.columns = data.keys()

    if table_name == 'un_docs':
        #exploding by sentence
        df['text_content'] = df['text_content'].apply(sent_tokenize)
        df = df.explode('text_content').reset_index(names='paragraph_index')
        
        # clean 
        df = df[df['text_content'].str.len() >= 30]

        df['text_content'] = df['text_content'].str.replace(r'\s+', ' ', regex=True) # remove spaces

        # remove nextlines
        df['text_content'] = df['text_content'].str.replace('\n',' ') 
        df['text_content'] = df['text_content'].str.replace('\x0c',' ')

        df = df[df['text_content'].str.len() >= 5]

        # typing
        df['text_content'] = df['text_content'].astype('str')
        df['sess'] = df['sess'].astype('int')
        df['year_created'] = df['year_created'].astype('int')
        df['country'] = df['country'].astype('str')

        # truncate (?)
        df = df[df['year_created'] >= 2007]

        # reset index
        df = df.drop('id', axis=1)
        df = df.reset_index(drop=True)
        df['id'] = df.index
                
    elif table_name == 'x_docs':
        # remove dupes
        df['dup'] = df['text_content'].apply(lambda x: x.split(' https')[0])
        df = df.drop_duplicates(subset=['dup'])
        df = df.drop('dup', axis=1)

        # reset index
        df = df.drop('id', axis=1)
        df = df.reset_index(drop=True)
        df['id'] = df.index

    """
    else:   # rep_docs
        (more processing)
    """

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
            if os.path.isfile('lib/'+self.table_name + '_' + filename + '.pickle'):
                with open('lib/'+self.table_name + '_' + filename + '.pickle','rb') as file:
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
            self.matrix = normalize(self.matrix, axis = 1)
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


    def query_fixer(self, token, counter=0):
            count = counter
            if ((count - 1) >= len(inv_pickled_dict[token])):
                return None
            if token in set(tfidf_vectorizer.get_feature_names_out()):
                return token
            else:
                if inv_pickled_dict[token][count] in set(tfidf_vectorizer.get_feature_names_out()):
                    return inv_pickled_dict[token][count]
                else:
                    return self.query_fixer(token, count+1)

    def vectorize_query(self,query:str):
        #TODO: Put in Spellchecker
        #TODO: JUAN PUT vec2querry; str -> list[(str, weight),]
        #DICT Key: token
        #Value diction
        query_list = list(word_tokenize(query))
        word_check = spell.unknown(query_list)
        new_query = ""

        for word in word_check:
            if type(spell.correction(word)) == str:
                query_list = [w.replace(word, spell.correction(word)) for w in query_list]

        # for token in query_list:
        #     new_token = self.query_fixer(token)
        #     if ((new_token != token) & (new_token != None)):
        #         query_list = [w.replace(token, new_token) for w in query_list]

        for word in query_list:
            new_query += word+" "
            
        
        return tfidf_vectorizer.transform([str(new_query),]) #+ take into account this weight
            

    def cossim(self,query:str) -> np.ndarray:
        # Returns an array, where array[n] represents the cosine similarity of the nth document
        query_vec = self.vectorize_query(self, query)
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
    """
        return np.array([cosine_similarity(matrix[doc_index,:],query_vec) 
                        if not np.sum(matrix[doc_index,:]) == 0 else 0 
                        for doc_index in range(0,matrix.shape[0])])
    """

    def svd_cossim(self, query:str, boolean_incentive = 1) -> np.ndarray:
        #vectorize query:
        
        query_vec = self.vectorize_query(self, query)
        if np.array_equal(query_vec, np.zeros(shape = query_vec.shape)): 
            return None

        # Returns an array, where array[n] represents the cosine similarity of the nth document
        svd_vec = normalize(np.dot(query_vec, self.svd_vt.T)).squeeze()

        #optional boolean search weight
        boolean_search_results = self.df['text_content'].str.lower().str.contains(query).values

        #we also slightly incentivize articles with the exact (stemmed wording)
        return np.multiply(self.svd_u.dot(svd_vec),(boolean_search_results * boolean_incentive) + 1)
    
    #big fail
    """
    def neighbors(self, query, limit):
        knn = NearestNeighbors(n_neighbors=limit, algorithm='auto', metric='cosine')
        knn.fit(self.matrix)
        
        query_vec = tfidf_vectorizer.transform([query])
        distances, indices = knn.kneighbors(query_vec)

        ret = []
        text_col = self.df['text_content']
        for i in range(len(indices[0])):
            ret.append(text_col[indices[0][i]])

        return ret
    """


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
        with open('lib/wordlist.pickle','wb') as file:
            pickle.dump(list(tfidf_vectorizer.get_feature_names_out()), file)
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
    with open('lib/wordlist.pickle','wb') as file:
        pickle.dump(list(tfidf_vectorizer.get_feature_names_out()), file)

    #Initialize tables
    #original min_df: 0.00005
    #NOTE: these parameters are manually optimized
    un_table = table(sql_engine,'un_docs',un_df,k=30)
    x_table = table(sql_engine,'x_docs',x_df, k=30)
    rep_table = table(sql_engine,'rep_docs',rep_df, k=30)