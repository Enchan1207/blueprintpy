#
# 引数レゾルバの基底クラス
#

"""
引数レゾルバの基底クラス
"""

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Set, Type

from blueprintpy.core import Argument


class Resolver(metaclass=ABCMeta):
    """
    Attributes:
        resolvers (Set[Type[Resolver]]) : 基底クラスを継承したResolverのセット
        __resolver_type__ (str): 引数レゾルバを特定するための名前
    """

    resolvers: Set[Type[Resolver]] = set()
    __resolver_type__: str = ""

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
