#
# ContentExtractorのテスト
#

import random
import string
import tempfile
from pathlib import Path
from unittest import TestCase

from src.pip_init import Argument, Content, ContentBuilder, ContentExtractor


class testContentExtractor(TestCase):

    def setUp(self) -> None:
        # テンプレートファイル置き場および展開先となる一時ディレクトリを生成
        template_root = tempfile.TemporaryDirectory()
        self.template_root = template_root
        self.template_root_path = Path(template_root.name)

        extract_root = tempfile.TemporaryDirectory()
        self.extract_root = extract_root
        self.extract_root_path = Path(extract_root.name)

    def tearDown(self) -> None:
        # 一時ディレクトリを削除
        self.template_root.cleanup()
        self.extract_root.cleanup()

    def testExtractPreparedContent(self):
        """ コンテンツの展開
        """

        # 1. バイナリファイルの展開 面倒なので直接生成します
        temp_bin_name = f"{self.random_strings(20)}.bin"
        temp_bin_content = random.randbytes(256)
        with open(self.template_root_path / temp_bin_name, "wb") as f:
            f.write(temp_bin_content)
        temp_bin = Content(temp_bin_name, str(self.extract_root_path / temp_bin_name))
        builder = ContentBuilder(str(self.template_root_path), str(self.extract_root_path), [])
        temp_bin_prepared = builder.build(temp_bin)
        ContentExtractor.extract(temp_bin_prepared)
        with open(self.extract_root_path / temp_bin_name, "rb") as f:
            extracted_content = f.read()
        self.assertEqual(temp_bin_content, extracted_content)

        # 2. テンプレートを通したファイルの展開
        arg_1 = Argument("arg_1", "argument for test")
        arg_1.value = "value of argument 1"

        temp_template_name = f"{self.random_strings(20)}.j2"
        temp_template_content = "{{arg_1}}"
        with open(self.template_root_path / temp_template_name, "w") as f:
            f.write(temp_template_content)
        temp_template = Content(temp_template_name, str(self.extract_root_path / "extracted.txt"))
        builder = ContentBuilder(str(self.template_root_path), str(self.extract_root_path), [arg_1])
        temp_template_prepared = builder.build(temp_template)
        ContentExtractor.extract(temp_template_prepared)
        with open(self.extract_root_path / "extracted.txt", "r") as f:
            extracted_content = f.read()
        self.assertEqual(arg_1.value, extracted_content)

    def random_strings(self, length: int) -> str:
        """指定された長さのランダムな文字列を生成する

        Args:
            length (int): 長さ

        Returns:
            str: 生成結果
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))
