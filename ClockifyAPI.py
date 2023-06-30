import requests
from User import User


class ClockifyAPI:

    def __init__(self, workspace_id: str):
        self.BASE_URL = 'https://api.clockify.me/api/v1/'
        self.workspace_id = workspace_id

    def _send_get_request(self, api_key: str, endpoint: str, params: dict[str, str] = None):
        headers = {
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        }
        url = self.BASE_URL + endpoint
        response = requests.get(url, headers=headers, params=params)
        if response.status_code >= 400:
            raise Exception(f"Request failed - {response.status_code}")
        data = response.json()

        return data

    def get_time_entries_per_user(self, user: User, start_date: str, end_date: str):
        endpoint = f'workspaces/{self.workspace_id}/user/{user.user_id}/time-entries'
        params = {
            'start': f'{start_date}T00:00:00Z',
            'end': f'{end_date}T23:59:59Z',
        }
        all_data = []
        page = 1

        while True:
            params['page'] = page
            response = self._send_get_request(user.api_key, endpoint, params)
            if len(response) == 0:
                break
            all_data.extend(response)
            page += 1

        return all_data

    def get_user_name(self, api_key: str):
        endpoint = f'user'
        get_user_data = self._send_get_request(api_key, endpoint)
        return get_user_data['name']
