#
# テンプレート構成のテスト
#

from json import JSONDecodeError
from unittest import TestCase

from src.blueprintpy.cli.config_loader import ConfigLoader


class testTemplateConfig(TestCase):

    def testLoadValidConfigFromJSON(self):
        """ JSON構成ファイルからConfigを生成
        """

        config_json_str = """
        {
            "name": "pip_init_basic",
            "args": [
                {
                    "name": "project_name",
                    "description": "The name of project"
                },
                {
                    "name": "dependencies",
                    "description": "Dependencies of project",
                    "argtype": "array"
                },
                {
                    "name": "mypy_python_version",
                    "description": "Version of Python3 interpreter (for mypy)",
                    "default_value": "3.9"
                }
            ],
            "contents": [
                {
                    "src": "setup.cfg",
                    "dest": "./setup.cfg"
                },
                {
                    "src": "setup.py",
                    "dest": "./setup.py"
                },
                {
                    "src": "__init__.py",
                    "dest": "./{project_name}/__init__.py"
                }
            ]
        }
        """
        ConfigLoader.load(config_json_str)

    def testLoadInValidConfigFromJSON(self):
        """ 不正なJSON構成ファイルからConfigを生成
        """

        # 1. jsonとして不適切 JSONDecodeError
        config_json_str = """
        """

        with self.assertRaises(JSONDecodeError):
            ConfigLoader.load(config_json_str)

        # 2. 要求キー不十分 KeyError
        config_json_str = """
        {
            "name": "invalid json"
        }
        """

        with self.assertRaises(KeyError):
            ConfigLoader.load(config_json_str)

        # 3. フォーマット不正 ValueError
        config_json_str = """
        {
            "name": "invalid json",
            "args": [
                {
                    "name": "project_name",
                    "description": "The name of project"
                },
                {
                    "name": "invalid args with insufficient params"
                },
                {
                    "name": "invalid args with unexpected params",
                    "invalid": ""
                }
            ],
            "contents":[

            ]
        }
        """

        with self.assertRaises(ValueError):
            ConfigLoader.load(config_json_str)

        # 4. インポート先不明 ImportError
        config_json_str = """
        {
            "name": "invalid json",
            "args": [
                {
                    "name": "project_name",
                    "description": "The name of project"
                }
            ],
            "args_handler": "src.invalid_module",
            "contents":[

            ]
        }
        """

        with self.assertRaises(ImportError):
            ConfigLoader.load(config_json_str)
