#
# コンフィグローダ
#
import importlib
from json.decoder import JSONDecoder
from typing import Optional

from blueprintpy.core import Argument, Config, Content


class ConfigLoader:
    """テンプレート構成ローダ
    """

    @staticmethod
    def load(config_json_str: str) -> Config:
        """json形式のテンプレート構成情報からテンプレート構成を生成します.

        Args:
            config_json_str (str): json形式のテンプレート構成情報

        Raises:
            KeyError: 構成情報に必要なプロパティが含まれていなかった場合.
            ValueError: 構成情報に不正な値が含まれていた場合.
            ModuleNotFoundError, ImportError: 引数ハンドラのインポートに失敗した場合.

        Returns:
            Config: 生成結果
        """

        # jsonデコード
        config_json = JSONDecoder().decode(config_json_str)

        # ルートに name, args, contentsがあることを期待する
        try:
            name, args, contents = tuple([config_json[key] for key in ['name', 'args', 'contents']])
        except KeyError:
            raise KeyError("name, args, and contents are required as root property of json.")

        # args, contentsはそれぞれインスタンスに起こす
        try:
            arg_instances = [Argument(**arg) for arg in args]
            content_instances = [Content(**content) for content in contents]
        except TypeError:
            raise ValueError("unexpected parameter of initilaize Argument or Content")

        # args_handlerが存在するならモジュールをロードする この時点でArgsHandlerBase.handlerからアクセスできるようになっているはず
        args_handler_path: Optional[str] = config_json['args_handler'] if 'args_handler' in config_json else None
        if args_handler_path is not None:
            importlib.import_module(args_handler_path)

        # Config生成
        return Config(name, arg_instances, content_instances, args_handler_path)
