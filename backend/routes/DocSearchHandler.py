from routes.helpers.DocSearchUN import doc_search_un_handler

def doc_search_handler(queryDocID,queryDocType,limit):
    from lib.Text_Processing_Utils import un_table, x_table, rep_table
    
    if queryDocType == 'un':
        query = un_table.df.loc[queryDocID]['text_content']
    elif queryDocType == 'x':
        query = x_table.df.loc[queryDocID]['text_content']
    elif queryDocType == 'rep':
        query = rep_table.df.loc[queryDocID]['text_content']

    # print(query)
    return doc_search_un_handler(query, limit)