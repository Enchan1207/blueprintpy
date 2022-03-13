#
# テンプレート引数
#

from typing import Optional


class Argument:
    """テンプレート引数
    """

    def __init__(self,
                 name: str,
                 description: str,
                 argtype: Optional[str] = None,
                 default_value: Optional[str] = None) -> None:
        """テンプレート引数を初期化します.

        Args:
            name (str): 引数名
            description (str): 引数の説明
            argtype (Optional[str], optional): 引数タイプ
            default_value (Optional[str], optional): デフォルト値
        """

        self.name = name
        self.description = description
        self.argtype = argtype
        self.default_value = default_value
