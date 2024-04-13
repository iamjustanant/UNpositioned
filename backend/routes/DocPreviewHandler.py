def doc_preview_handler(sql_engine,queryDocID,queryDocType):
  #TODO: Implement this function to return a PREVIEW of the document with the given ID and type (probably just the most relevant sentence)
  if queryDocType == 'UN':
    row = un_table.df.loc[queryDocID]
    return row['text_content']
  elif queryDocType == 'X':
    row = x_table.df.loc[queryDocID]
    return x_table.df.loc[queryDocID]['text_content']
  elif queryDocType == 'Rep':
    row = rep_table.df.loc[queryDocID]
    return rep_table.df.loc[queryDocID]['text_content']
  else:
    return None