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
    
    
    #big fail
    """
    if queryDocType == 'un':
        query = un_table.df.loc[queryDocID]['text_content']
        if desiredType == 'un':
            return un_table.neighbors(query, limit)
        elif desiredType == 'x':
            return x_table.neighbors(query, limit)
        elif desiredType == 'rep':
            return rep_table.neighbors(query, limit)
        else:
            return ['invalid desiredType']
        
    elif queryDocType == 'x':
        query = x_table.df.loc[queryDocID]['text_content']
        if desiredType == 'un':
            return un_table.neighbors(query, limit)
        elif desiredType == 'x':
            return x_table.neighbors(query, limit)
        elif desiredType == 'rep':
            return rep_table.neighbors(query, limit)
        else:
            return ['invalid desiredType']
        
    elif queryDocType == 'rep':
        query = rep_table.df.loc[queryDocID]['text_content']
        if desiredType == 'un':
            return un_table.neighbors(query, limit)
        elif desiredType == 'x':
            return x_table.neighbors(query, limit)
        elif desiredType == 'rep':
            return rep_table.neighbors(query, limit)
        else:
            return ['invalid desiredType']
    
    else:
        return ['invalid queryDocType']
    """