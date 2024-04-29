import numpy as np

def doc_search_x_handler(text,limit):
  from lib.Text_Processing_Utils import x_table

  cossim_results = x_table.cossim(text)
  svd_results = x_table.svd_cossim(text)

  if cossim_results is not None and svd_results is not None:
    
    # Formatted output
    ttic = [
      # ID, Followers, Verified, User Name, Text Content
      f"{id}||| {int(flw)} ||| {bool(ver)} ||| {user} said: {tc}" 
       for id, flw, ver, user, tc in x_table.df[['id', 'followers', 'verified', 
                                                 'user_name', 'text_content']].iloc
                                                 [np.lexsort((svd_results,cossim_results))][::-1][:limit].values
    ]
    return ttic
  
  else:
    return ['No relevant results found :(',]
  