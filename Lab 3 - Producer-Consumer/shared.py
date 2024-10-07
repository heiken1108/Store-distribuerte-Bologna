import datetime

class Data:
    def __init__(
        self,
        n: json.dumps,
        created_by: str,
        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):
        self.n = n
        self.created_by = created_by
        self.created_at = created_at

    def __str__(self):
        return f"Data: {self.__dict__}"
