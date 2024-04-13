from backend.routes.helpers.DocSearchRep import doc_search_rep_handler
from backend.routes.helpers.DocSearchUN import doc_search_un_handler
from backend.routes.helpers.DocSearchX import doc_search_x_handler

def term_search_handler(sql_engine,queryStr,desiredType,limit):
  if (desiredType == 'UN'):
    return doc_search_un_handler(sql_engine,queryStr,limit)
  elif (desiredType == 'X'):
    return doc_search_x_handler(sql_engine,queryStr,limit)
  elif (desiredType == 'Rep'):
    return doc_search_rep_handler(sql_engine,queryStr,limit)
