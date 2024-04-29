import numpy as np

def doc_search_rep_handler(text,limit):
  from lib.Text_Processing_Utils import rep_table

  cossim_results = rep_table.cossim(text)
  svd_results = rep_table.svd_cossim(text)

  if cossim_results is not None or svd_results is not None:
    
    # Formatted output
    ttic = [
      # ID, Audience, Bias Confidence, Bias, Author said on medium content
       f"{id}||| {aud} ||| {int(bc * 100)} ||| {b} ||| {author} said on {ms.upper()}: {tc}" 
       for id, aud, bc, b, ms, author, tc in  rep_table.df[['id', 'audience', 'bias_conf', 'bias', 
                                                            'media_source','author','text_content']].iloc
                                                            [np.lexsort((svd_results,cossim_results))][::-1][:limit].values
    ]
    return ttic
  
  else:
    return ['No relevant results found :(',]
