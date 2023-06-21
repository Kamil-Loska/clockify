import configparser
from typing import Dict


class ConfigFileHandler:

    def __init__(self, config_file: str):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.config.read(config_file)

    def get_workspace_id(self) -> str:
        return self.config.get('Clockify', 'WORKSPACE_ID')

    def translation_mapper(self) -> Dict[str, str]:
        field_mappings = self.config['FIELDINFO']
        translation_mapping = {key: value for key, value in field_mappings.items()}
        return translation_mapping
