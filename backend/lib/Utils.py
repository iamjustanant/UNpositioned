import json

def parseBool(v):
  if v is None:
      return None
  return v.lower() in ("yes", "true", "t", "1")

def parseInt(v):
  if v is None:
      return None
  return int(v)

def parseArg(str):
  return str.replace("+"," ")

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