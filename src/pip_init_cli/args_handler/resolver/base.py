#
# 引数レゾルバの規定クラス
#

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Set, Type

from pip_init import Argument


class Resolver(metaclass=ABCMeta):
    """引数レゾルバ
    """

    resolvers: Set[Type[Resolver]] = set()
    __argtype__: str = ""

    def __init_subclass__(cls) -> None:
        super.__init_subclass__()

        cls.resolvers.add(cls)

    @staticmethod
    @abstractmethod
    def resolve(argument: Argument) -> Argument:
        """与えられたテンプレート引数に適切な値を代入します.

        Args:
            argument (Argument): 対象のテンプレート引数

        Returns:
            Argument: 代入結果
        """
        raise NotImplementedError()
