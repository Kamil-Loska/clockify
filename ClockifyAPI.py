import requests


class ClockifyAPI:

    def __init__(self, workspace_id):
        self.BASE_URL = 'https://api.clockify.me/api/v1/'
        self.workspace_id = workspace_id

    def send_get_request(self, api_key, endpoint, params=None):
        headers = {
            'X-Api-Key': api_key,
            'Content-Type': 'application/json'
        }
        url = self.BASE_URL + endpoint
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        return data

    def get_time_entries_per_user(self, api_key, user_id, start_date, end_date):
        endpoint = f'workspaces/{self.workspace_id}/user/{user_id}/time-entries'
        params = {
            'start': f'{start_date}T00:00:00Z',
            'end': f'{end_date}T23:59:59Z',
        }
        all_data = []
        page = 1

        while True:
            params['page'] = page
            response = self.send_get_request(api_key, endpoint, params)
            if len(response) == 0:
                break

            all_data.extend(response)
            page += 1

        return all_data

    def get_user_name(self, api_key):
        endpoint = f'user'
        get_user_data = self.send_get_request(api_key, endpoint)
        return get_user_data['name']
