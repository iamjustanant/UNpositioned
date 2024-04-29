import numpy as np

def doc_search_un_handler(text,limit):
  from lib.Text_Processing_Utils import un_table

  cossim_results = un_table.cossim(text)
  svd_results = un_table.svd_cossim(text)

  if svd_results is not None and cossim_results is not None:
    # Formatted output
    ttic = [
       f"{id}|||In {year}, {country} said: {tc}" 
       for id, country, year, tc in un_table.df[['id','country','year_created','text_content']].iloc
       [np.lexsort((svd_results,cossim_results))][::-1][:limit].values
    ]
    return ttic
  
  else:
    return ['No relevant results found :(',]