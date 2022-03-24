#
# コンフィグシリアライザ
#
from functools import reduce
from typing import Any, Dict

from blueprintpy.core import Config


class ConfigSerializer:
    """テンプレート構成シリアライザ
    """

    @staticmethod
    def serialize(config: Config) -> Dict[str, Any]:
        """テンプレート構成オブジェクトをシリアライズし、辞書形式に変換します.

        Args:
            config (Config): シリアライズする構成オブジェクト

        Returns:
            Dict[str, Any]: シリアライズ結果
        """

        serialized: Dict[str, Any] = {}

        # 名前はそのまま
        serialized['name'] = config.name

        # Argumentは適当に処理する valueはコンストラクタにないのでスルー
        serialized_args = [
            reduce(
                lambda p, n: p | n,
                list(
                    [{key: getattr(arg, key)}
                     if getattr(arg, key) is not None else{} for key in ['name', 'description', 'argtype', 'default_value']]))
            for arg in config.args]
        serialized['args'] = serialized_args

        # ハンドラはそのまま ただし存在しなければ追加しない
        if config.args_handler_name is not None:
            serialized['args_handler'] = config.args_handler_name

        # Contentも同様
        serialized_contents = [{'src': content.src, 'dest': content.dest} for content in config.contents]
        serialized['contents'] = serialized_contents

        return serialized
