#
# テンプレート構成のテスト
#

from unittest import TestCase

from src.pip_init.args_handler import DefaultArgsHandler
from src.pip_init.config import Config


class testTemplateConfig(TestCase):

    def testInstantiateConfig(self):
        handler = DefaultArgsHandler()
        config = Config("", [], [], handler)
        print(config)
