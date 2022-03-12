#
# テンプレートjsonローダ
#

from json.decoder import JSONDecodeError, JSONDecoder
from typing import List

from .models import Argument, Config, Content


class ConfigLoader:
    """テンプレート構成ファイルのローダー
    """

    __loader_errors__ = (ValueError, JSONDecodeError, KeyError, TypeError)

    @staticmethod
    def load(config_json_str: str) -> Config:
        """構成ファイルからテンプレートコンフィグを生成します.

        Args:
            config_json_str (str): 構成ファイルの内容

        Raises:
            ValueError: 不正な値が渡された場合.
            JSONDecodeError: 構成ファイルのパースに失敗した場合.
            KeyError: 必要な情報が構成ファイルに与えられなかった場合.
            TypeError: 

        Returns:
            Config: 生成結果
        """

        # ファイルの内容をjsonパース
        config_json = JSONDecoder().decode(config_json_str)

        # name, args, contentsが存在することを期待
        name, args, contents = tuple([config_json[key] for key in ['name', 'args', 'contents']])

        # args, contentsはさらにArgumentインスタンスに起こす
        argument_instances: List[Argument] = [Argument(**arg) for arg in args]
        contents_instances: List[Content] = [Content(**content) for content in contents]

        # arg_handlerはなければデフォルト あれば動的import

        raise NotImplementedError()
