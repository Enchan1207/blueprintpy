#
# ContentBuilderのテスト
#

import os
import random
import string
import tempfile
from functools import reduce
from json import JSONDecoder
from json.encoder import JSONEncoder
from pathlib import Path
from typing import List
from unittest import TestCase

from src.pip_init.argument import Argument
from src.pip_init.config import Config
from src.pip_init.content import Content
from src.pip_init.content_builder import ContentBuilder
from src.pip_init.loader import ConfigLoader
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

        # 適当な名前のテンプレート引数を生成し、値を設定
        args_mock = [Argument(f"arg_{n}", self.random_strings(20), self.random_strings(5), self.random_strings(20)) for n in range(10)]
        for arg in args_mock:
            arg.value = self.random_strings(30)

        # 適当なコンテンツを生成
        contents_mock: List[Content] = []
        for n in range(10):
            # コンテンツが指す一時ファイルのパスを作って
            temp_content_name = f"content_{n}_{self.random_strings(20)}"
            temp_content_path = self.template_root_path / temp_content_name

            # モックに追加 わかりにくいですが "{引数名}" を生成しています
            contents_mock.append(Content(str(temp_content_path), f"./{{{args_mock[n].name}}}"))

            # 一時ファイルの実体を生成 値はargsの中身
            with open(temp_content_path, "w") as f:
                args_serialized = reduce(
                    lambda p, n: p | n,
                    list(
                        [{key: getattr(args_mock[n], key)}
                         if getattr(args_mock[n], key) is not None else {} for key in ['name', 'description', 'argtype', 'default_value']]))
                f.write(JSONEncoder().encode(args_serialized))

        # Configを生成
        conf_name = "config for unittest"
        config = Config(conf_name, args_mock, contents_mock)

        # シリアライザでDictに変換 jsonで保存してもよいがすぐロードするので今回はスルー
        serialized = ConfigSerializer.serialize(config)
        encoded = JSONEncoder().encode(serialized)

        # ConfigLoaderにより構成をロード
        loaded_config = ConfigLoader.load(encoded)

        # ビルダーに通す
        builder = ContentBuilder(self.template_root_path, "./", args_mock, None)
        prepared_contents = [builder.build(content) for content in loaded_config.contents]

        # ビルド結果を照合
        for prepared, origin, arg in zip(prepared_contents, contents_mock, args_mock):
            # オブジェクトの状態
            self.assertEqual(prepared.source, Path(origin.src))
            self.assertEqual(prepared.dest_path, Path(arg.value))

            # ファイルの中身
            with open(prepared.source) as f:
                arg_in_file = Argument(**JSONDecoder().decode(f.read()))
                [self.assertEqual(getattr(arg_in_file, key), getattr(arg, key))
                 for key in ['name', 'description', 'argtype', 'default_value']]

    def testBuildContentWithJinja(self):
        """jinjaテンプレートを含むテンプレートのビルドと展開
        """

        # 適当にテンプレート引数を生成
        args_mock = [Argument(f"arg_{n}", self.random_strings(20), self.random_strings(5), self.random_strings(20)) for n in range(10)]
        for arg in args_mock:
            arg.value = self.random_strings(30)

        # 引数はひとつだけ特殊なのを入れておく
        array_arg = Argument("array_test", "", "array", None)
        array_arg.value = [arg.value for arg in args_mock]
        args_mock.append(array_arg)

        # テンプレートコンテンツはちょっと手を入れる
        contents_mock: List[Content] = []

        # 1. 拡張子 .j2 のファイルを生成 中身は各引数の名前(つまり値が展開されるはず)
        template_1 = "".join([f"{{{{ {arg.name} }}}}" for arg in args_mock[0:len(args_mock) - 1]])
        template_1_name = f"{self.random_strings(10)}.j2"
        template_1_path = str(self.template_root_path / f"{template_1_name}")
        content_1 = Content(template_1_name, "")
        contents_mock.append(content_1)
        with open(template_1_path, "w") as f:
            f.write(template_1)

        # 2. 拡張子ではなくイニシャライザで明示的にテンプレート処理を要求, テンプレ内ではArgumentで渡された配列を展開
        template_2 = "{% for i in array_test %}{{ i }}{% endfor %}"
        template_2_name = f"{self.random_strings(10)}"
        template_2_path = str(self.template_root_path / f"{template_2_name}")
        content_2 = Content(template_2_name, "", True)
        contents_mock.append(content_2)
        with open(template_2_path, "w") as f:
            f.write(template_2)

        # コンフィグを生成し、ビルダーに通す
        conf_name = "config for unittest"
        config = Config(conf_name, args_mock, contents_mock)
        builder = ContentBuilder(str(self.template_root_path), "./", args_mock, None)
        prepared_contents = [builder.build(content) for content in config.contents]

        # コンテンツが保持するデータを取得 これらは同じ値を示すはず
        for content in prepared_contents:
            self.assertIsNotNone(content.extract_object)
        self.assertEqual(prepared_contents[0].extract_object, prepared_contents[1].extract_object)

    def random_strings(self, length: int) -> str:
        """指定された長さのランダムな文字列を生成する

        Args:
            length (int): 長さ

        Returns:
            str: 生成結果
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))
