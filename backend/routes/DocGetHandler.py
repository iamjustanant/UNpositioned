def doc_get_handler(queryDocID,queryDocType):
  from lib.Text_Processing_Utils import un_table, x_table, rep_table

  if queryDocType == 'un':
    row = un_table.df.loc[queryDocID]
    country, year, tc = row[['country','year_created','text_content']]
    paragraph = " ".join(un_table.df[un_table.df['paragraph_index'] == row['paragraph_index']]['text_content'].values)
    ttic = [
       f"In {year}, {country} said: {paragraph}" 
    ]
    return ttic
    
  elif queryDocType == 'x':
    row = x_table.df.loc[queryDocID]
    id, flw, ver, user, tc = row[['id', 'followers', 'verified', 'user_name', 'text_content']]
    ttic = [
      f"{id}||| {int(flw)} ||| {bool(ver)} ||| {user} said: {tc}"
    ]
    return ttic
  
  elif queryDocType == 'rep':
    row = rep_table.df.loc[queryDocID]
    id, aud, bc, b, ms, author, tc = row[['id', 'audience', 'bias_conf', 'bias', 'media_source','author','text_content']]
    ttic = [
       f"{id}||| {aud} ||| {int(bc * 100)} ||| {b} ||| {author} said on {ms.upper()}: {tc}" 
    ]
    return ttic
  
  else:
    return ['type error']