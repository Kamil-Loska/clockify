class User:
    def __init__(self, user_id: str, api_key: str, department: str):
        self._user_id = user_id
        self._api_key = api_key
        self._department = department

    @property
    def user_id(self):
        return self._user_id

    @property
    def api_key(self):
        return self._api_key

    @property
    def department(self):
        return self._department
