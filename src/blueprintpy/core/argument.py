#
# テンプレート引数
#

from typing import Any, Optional


class Argument:
    """パッケージテンプレート内で展開される引数.
    """

    def __init__(self,
                 name: str,
                 description: str,
                 argtype: Optional[str] = None,
                 default_value: Optional[str] = None) -> None:
        """
        Args:
            name (str): 引数名
            description (str): 引数の説明
            argtype (Optional[str], optional): 引数タイプ
            default_value (Optional[str], optional): デフォルト値

        Note:
            :code:`argtype` パラメータは引数の型を示します.
            blueprintpy コアモジュールでは利用されませんが、CLIツールのデフォルト引数ハンドラでは対応する名称の
            レゾルバ (:mod:`blueprintpy.cli.args_handler.resolver`) を呼び出そうとします.
        """

        self.name = name
        self.description = description
        self.argtype = argtype
        self.default_value = default_value
        self.value: Any = None
