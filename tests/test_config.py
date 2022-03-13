#
# テンプレート構成のテスト
#

from unittest import TestCase

from src.pip_init.args_handler import DefaultArgsHandler
from src.pip_init.config import Config
from src.pip_init.loader import ConfigLoader


class testTemplateConfig(TestCase):

    def testInstantiateConfig(self):
        """ 単純なインスタンス化 importステートメントの確認
        """

        handler = DefaultArgsHandler()
        print(handler.handlers)

        config = Config("", [], [])
        print(config)

    def testLoadConfigFromJSON(self):
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
            "args_handler": "src.pip_init.args_handler.default",
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
        config = ConfigLoader.load(config_json_str)
        print(config)
