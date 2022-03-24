#
# 引数ハンドラ基底クラス
#

"""
テンプレート引数ハンドラの基底クラス
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import List, Set, Type

from blueprintpy.core import Argument


class ArgsHandlerBase(metaclass=ABCMeta):
    """
    Attributes:
        handlers (Set[Type[ArgsHandlerBase]]) : 基底クラスを継承したArgsHandlerのセット
        __handler_name__ (str): 引数ハンドラを特定するための名前
    """

    handlers: Set[Type[ArgsHandlerBase]] = set()
    __handler_name__: str = ""

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        cls.handlers.add(cls)

    @staticmethod
    @abstractmethod
    def handle_args(args: List[Argument]) -> List[Argument]:
        """与えられたテンプレート引数リストに適切な値を挿入します。

        Args:
            args (List[Argument]): 対象のテンプレート引数リスト

        Returns:
            List[Argument]: 挿入結果
        """
