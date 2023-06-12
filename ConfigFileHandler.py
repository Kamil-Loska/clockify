import configparser


class ConfigFileHandler:

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_workspace_id(self):
        return self.config.get('Clockify', 'WORKSPACE_ID')

    def translation_mapper(self):
        field_mappings = self.config['FIELDINFO']
        translation_mapping = {key.title(): value for key, value in field_mappings.items()}
        return translation_mapping
