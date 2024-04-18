def doc_get_handler(sql_engine,queryDocID,queryDocType):
  # TODO: Implement this function to return the FULL document with the given ID and type
  #TODO: Implement this function to return a PREVIEW of the document with the given ID and type (probably just the most relevant sentence)

  if queryDocType == 'UN':
    row = un_table.df.loc[queryDocID]

    paragraph = " ".join(un_table.df[un_table.df['paragraph_index'] == row['paragraph_index']]['text_content'].values)
    return row['country_name'] + ', ' + row['year'] + ': '  + paragraph
    
  elif queryDocType == 'X':
    row = x_table.df.loc[queryDocID]
    return row['text_content']
  elif queryDocType == 'Rep':
    row = rep_table.df.loc[queryDocID]
    return row['text_content']
  else:
    return None