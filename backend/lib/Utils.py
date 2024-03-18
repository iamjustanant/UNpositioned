def parseBool(v):
  if v is None:
      return None
  return v.lower() in ("yes", "true", "t", "1")

def parseInt(v):
  if v is None:
      return None
  return int(v)