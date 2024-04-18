from routes.helpers.DocSearchRep import doc_search_rep_handler
from routes.helpers.DocSearchUN import doc_search_un_handler
from routes.helpers.DocSearchX import doc_search_x_handler

def term_search_handler(sql_engine,queryStr,desiredType,limit):
  if (desiredType == 'un'):
    return doc_search_un_handler(sql_engine,queryStr,limit)
  elif (desiredType == 'x'):
    return doc_search_x_handler(sql_engine,queryStr,limit)
  elif (desiredType == 'rep'):
    return doc_search_rep_handler(sql_engine,queryStr,limit)
  else:
    raise TypeError("Type must be un x or rep")
