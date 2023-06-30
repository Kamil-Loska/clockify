class User:
    def __init__(self, user_id: str, api_key: str):
        self._user_id = user_id
        self._api_key = api_key

    @property
    def user_id(self):
        return self._user_id

    @property
    def api_key(self):
        return self._api_key
