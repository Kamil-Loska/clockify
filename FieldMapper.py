from typing import Iterator
from ConfigFileHandler import ConfigFileHandler


class FieldMapper:
    def __init__(self, config_handler: ConfigFileHandler):
        self.translation_map = config_handler.translation_mapper()

    def map_fields(self, report_data: list[dict[str, str]]) -> Iterator[dict[str, str]]:
        for entry in report_data:
            yield {self.translation_map.get(key, key): value for key, value in entry.items()}
