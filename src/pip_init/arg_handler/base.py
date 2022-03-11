#
# 引数ハンドラの基底クラス
#

from __future__ import annotations
from typing import List, Set, Type

from ..models import Argument


class ArgumentHandlerBase:
    """引数ハンドラの基底クラス

    Attributes:
        argument_handlers (Set[Type[ArgumentHandlerBase]]) : 基底クラスを継承したArgumentHandlerのセット
    """
    argument_handlers: Set[Type[ArgumentHandlerBase]] = set()

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        cls.argument_handlers.add(cls)

    @staticmethod
    def handle_args(args: List[Argument]) -> List[Argument]:
        """引数に渡されたテンプレート引数を処理し、その結果を返します.

        Args:
            args (List[Argument]): テンプレート引数のリスト

        Returns:
            List[Argument]: 処理結果
        """
        raise NotImplementedError()
