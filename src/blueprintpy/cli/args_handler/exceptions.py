#
# 引数ハンドリング例外
#
"""引数の処理過程で発生する例外
"""

from blueprintpy.core import Argument


class ArgumentHandlingError(Exception):
    """(基底クラス)
    """


class ValidationError(ArgumentHandlingError):
    """引数に渡された値が不正だった場合に発生する例外.
    """

    def __init__(self, argument: Argument, reason: str) -> None:
        self.argument = argument
        self.reason = reason
        super().__init__(argument, reason)
