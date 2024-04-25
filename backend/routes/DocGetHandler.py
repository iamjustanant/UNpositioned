from routes.helpers.DocSearchUN import country_map

def doc_get_handler(queryDocID,queryDocType):
  #TODO: Implement this function to return the FULL document with the given ID and type
  from lib.Text_Processing_Utils import un_table, x_table, rep_table

  if queryDocType == 'un':
    row = un_table.df.loc[queryDocID]
    country, year, tc = row[['country','year_created','text_content']]
    paragraph = " ".join(un_table.df[un_table.df['paragraph_index'] == row['paragraph_index']]['text_content'].values)
    ttic = [
       f"In {year}, {country_map(country).upper()} said: {paragraph}" 
    ]
    return ttic
    
  elif queryDocType == 'x':
    row = x_table.df.loc[queryDocID]
    user, tc = row[['user_name', 'text_content']]
    ttic = [
      f"{user} said: {tc}" 
    ]
    return ttic
  
  elif queryDocType == 'rep':
    row = rep_table.df.loc[queryDocID]
    ms, author, tc = row[['media_source','author','text_content']]
    ttic = [
       f"{author} said on {ms.upper()}: {tc}" 
    ]
    return ttic
  
  else:
    return ['type error']