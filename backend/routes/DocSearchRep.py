# TODO: Write the `doc_search_un_handler` function that takes as input
# - search text (string)
# - an optional limit parameter (int) to limit the number of results, defaulting to 10
# The function should return the most relevant UN positions.
# Of course, the first parameter provided is the SQL Engine itself, which lets you execute SQL queries on the database.

def doc_search_rep_handler(sql_engine,text,limit):
  # Naive implementation here for now
  my_sql_query = "SELECT * FROM rep_docs"
  if text:
    my_sql_query += " WHERE text_content LIKE '%" + text + "%'"
  if limit:
    my_sql_query += " LIMIT " + str(limit)
  my_sql_query += ";"

  data = sql_engine.query_selector(my_sql_query)
  return data


  
  
