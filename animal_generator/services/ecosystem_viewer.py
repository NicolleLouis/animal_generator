import json
from pathlib import Path


class EcosystemViewer:
    ecosystem_directory_name = 'list_ecosystem'

    @classmethod
    def find_ecosystem(cls, name):
        list_ecosystem = cls.find_list_ecosystem()
        ecosystems = list_ecosystem.iterdir()
        for ecosystem_file in ecosystems:
            with open(ecosystem_file) as json_data:
                ecosystem = json.load(json_data)
                if ecosystem["name"] == name:
                    return ecosystem
        raise EcosystemViewerException("Ecosystem Not Found")

    @classmethod
    def find_list_ecosystem(cls):
        base_directory = Path(__file__).resolve().parent.parent
        for file in base_directory.iterdir():
            if file.name == cls.ecosystem_directory_name:
                return file
        raise EcosystemViewerException("Ecosystem Directory Not Found")


class EcosystemViewerException(Exception):
    """All Zoo Viewer Exceptions"""
