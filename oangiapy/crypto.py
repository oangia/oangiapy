import hashlib

def md5(text):
  text_bytes = text.encode('utf-8')
  return hashlib.md5(text_bytes).hexdigest()
