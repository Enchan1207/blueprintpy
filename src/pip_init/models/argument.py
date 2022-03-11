#
# テンプレートに挿入する引数
#
from typing import Any, Optional


class Argument:
    """テンプレートに挿入する引数
    """

    def __init__(self,
                 name: str,
                 description: str,
                 default_value: Optional[Any] = None,
                 arg_type: Optional[str] = "str") -> None:
        """テンプレート引数を生成します.

        Args:
            name (str): 引数名
            description (str): 引数の説明
            default_value (Optional[Any], optional): デフォルト値
            arg_type (Optional[str], optional): 引数タイプ
        """

        self.name = name
        self.description = description
        self.default_value = default_value
        self.arg_type = arg_type

        self.value: Optional[Any] = default_value
