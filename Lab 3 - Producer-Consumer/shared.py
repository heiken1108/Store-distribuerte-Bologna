import json, datetime

class Data():
  def __init__(self, n: json.dumps, created_by: str):
    self.n = n
    self.created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.created_by = created_by

  def __str__(self):
    return f"Data: {self.__dict__}"