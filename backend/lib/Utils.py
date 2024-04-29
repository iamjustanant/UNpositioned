import json
import numpy as np

def parseBool(v):
  if v is None:
      return None
  return v.lower() in ("yes", "true", "t", "1")

def parseInt(v):
  if v is None:
      return None
  return int(v)

def parseArg(str):
  if str is None:
        return ""
  return str.replace("+"," ")

def sparse_argsort(arr:np.ndarray): #argsort while excluding zeros
    #https://stackoverflow.com/questions/40857349/np-argsort-which-excludes-zero-values
    indices = np.nonzero(arr)[0]
    return indices[np.argsort(arr[indices])]

def formatServerResponse(data):
  try:
      formatted_data = [list(row) if isinstance(row, tuple) else row for row in data]
  except Exception as e:
      formatted_data = data

  return json.dumps(
      {
          'res': formatted_data,
      },
      indent=4, sort_keys=True, default=str
  )