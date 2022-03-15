#
# ContentBuilderのテスト
#

import os
from pathlib import Path
import tempfile
from typing import List
from unittest import TestCase
from src.pip_init.argument import Argument

from json.encoder import JSONEncoder
from src.pip_init.config import Config
from src.pip_init.content import Content
from src.pip_init.serializer import ConfigSerializer


class testContentBuilder(TestCase):

    def setUp(self) -> None:
        # テンプレートファイル置き場となる一時ディレクトリを生成
        template_root = tempfile.TemporaryDirectory()
        self.template_root = template_root
        self.template_root_path = Path(template_root.name)

    def tearDown(self) -> None:
        # 一時ディレクトリを削除
        self.template_root.cleanup()

    def testBuildContent(self):
        """ ContentBuilderのビルドテスト
        """

        # 適当に構成を作って、
        conf_name = "config for unittest"
        conf_args: List[Argument] = []
        conf_contents: List[Content] = []
        config = Config(conf_name, conf_args, conf_contents)

        # シリアライザでDictに変換して、jsonで保存
        serialized = ConfigSerializer.serialize(config)
        encoded = JSONEncoder().encode(serialized)
        with open(self.template_root_path / "template.json", 'w') as f:
            f.write(encoded)

        #
