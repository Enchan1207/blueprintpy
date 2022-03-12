#
# configローダのテスト
#

from unittest import TestCase

from src.pip_init.config_loader import ConfigLoader


class testConfigLoader(TestCase):

    def test_loadconfig(self):
        config_json = """
        {
            "name": "template json for testing",
            "args": [
                {
                    "name": "project_name",
                    "description": "The name of project"
                },
                {
                    "name": "python_version_for_mypy",
                    "description": "Python interpreter version for mypy.ini",
                    "default_value": "3.9"
                }
            ],
            "contents": [
                {
                    "source_path": "setup.cfg",
                    "dest_path": "./setup.cfg"
                },
                {
                    "source_path": "setup.py",
                    "dest_path": "./setup.py"
                },
                {
                    "source_path": "__init__.py",
                    "dest_path": "./{project_name}/__init__.py"
                }
            ]
        }
        """
        config = ConfigLoader.load(config_json)
