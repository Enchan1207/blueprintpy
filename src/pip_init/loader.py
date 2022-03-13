#
# コンフィグローダ
#
import importlib
from json.decoder import JSONDecoder
from typing import Optional

from src.pip_init.argument import Argument
from src.pip_init.content import Content
from .config import Config


class ConfigLoader:
    """テンプレート構成ローダ
    """

    @staticmethod
    def load(config_json_str: str) -> Config:
        """json形式のテンプレート構成情報からテンプレート構成を生成します.

        Args:
            config_json_str (str): json形式のテンプレート構成情報

        Returns:
            Config: 生成結果
        """

        # jsonデコード
        config_json = JSONDecoder().decode(config_json_str)

        # ルートに name, args, contentsがあることを期待する
        name, args, contents = tuple([config_json[key] for key in ['name', 'args', 'contents']])

        # args, contentsはそれぞれインスタンスに起こす
        arg_instances = [Argument(**arg) for arg in args]
        content_instances = [Content(**content) for content in contents]

        # args_handlerが存在するならモジュールをロードする この時点でArgsHandlerBase.handlerからアクセスできるようになっているはず
        args_handler_path: Optional[str] = config_json['args_handler'] if 'args_handler' in config_json else None
        if args_handler_path is not None:
            importlib.import_module(args_handler_path)

        # Config生成
        return Config(name, arg_instances, content_instances)
