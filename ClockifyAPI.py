import requests
from FileHandler import FileHandler


class ClockifyAPI:

    def __init__(self):
        self.API_KEY = ''
        self.USER_ID = ''

        self.BASE_URL = 'https://api.clockify.me/api/v1/'
        self.file_handler = FileHandler()

    def send_get_request(self, endpoint, params=None):
        headers = {
            'X-Api-Key': self.API_KEY,
            'Content-Type': 'application/json'
        }
        url = self.BASE_URL + endpoint
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        return data

    def get_time_entries_per_user(self, start_date, end_date):
        workspace_id = self.file_handler.config['Clockify'].get('WORKSPACE_ID')
        endpoint = f'workspaces/{workspace_id}/user/{self.USER_ID}/time-entries'
        params = {
            'start': f'{start_date}T00:00:00Z',
            'end': f'{end_date}T23:59:59Z',
        }
        all_data = []
        page = 1

        while True:
            params['page'] = page
            response = self.send_get_request(endpoint, params)
            if len(response) == 0:
                break

            all_data.extend(response)
            page += 1

        return all_data

    def get_time_entries_per_user(self, start_date, end_date):
        workspace_id = self.file_handler.config['Clockify'].get('WORKSPACE_ID')
        endpoint = f'workspaces/{workspace_id}/user/{self.USER_ID}/time-entries'
        params = {
            'start': f'{start_date}T00:00:00Z',
            'end': f'{end_date}T23:59:59Z',
        }
        all_data = []
        page = 1

        while True:
            params['page'] = page
            response = self.send_get_request(endpoint, params)
            if len(response) == 0:
                break

            all_data.extend(response)
            page += 1

        return all_data

    def get_user_data(self):
        endpoint = f'user'
        get_user_data = self.send_get_request(endpoint)
        return get_user_data['id'], get_user_data['name']
