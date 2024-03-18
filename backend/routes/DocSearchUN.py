# TODO: Write the `doc_search_un_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# - an optional agree parameter (boolean) to filter for documents that agree with the search text (if true), and oppose the search text (if false)
#   if not provided, simply return the top relevant documents regardless of whether they agree or disagree with the search text!
# The functions should return
# - The top `limit` documents most relevant to the search `text`, filtered depending on `agree`, as a JSON list of objects, each with the following keys:
#   - `country` (string): the country of the document
#   - `year` (int): the year of the document
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

def doc_search_un_handler(sql_engine,text,limit,agree):
  
  
