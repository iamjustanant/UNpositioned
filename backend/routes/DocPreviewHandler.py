from routes.DocGetHandler import doc_get_handler

def doc_preview_handler(queryDocID,queryDocType):
  from lib.Text_Processing_Utils import un_table

  if queryDocType == 'un':
    row = un_table.df.loc[queryDocID]
    country, year, tc = row[['country','year_created','text_content']]
    ttic = [
       f"In {year}, {country} said: {tc}" 
    ]
    return ttic
  
  else:
    return doc_get_handler(queryDocID, queryDocType)