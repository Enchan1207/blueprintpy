#
# 引数ハンドラ基底クラス
#

from abc import ABCMeta, abstractmethod
from typing import List

from ..argument import Argument


class ArgsHandlerBase(metaclass=ABCMeta):
    """テンプレート引数ハンドラ
    """

    @abstractmethod
    @staticmethod
    def handle_args(args: List[Argument]) -> List[Argument]:
        """与えられたテンプレート引数リストに適切な値を挿入します。

        Args:
            args (List[Argument]): 対象のテンプレート引数リスト

        Returns:
            List[Argument]: 挿入結果
        """
