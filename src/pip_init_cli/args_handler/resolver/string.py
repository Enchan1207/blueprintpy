#
# 単純な文字列
#
from pip_init import Argument

from .base import Resolver


class StringResolver(Resolver):
    """単純な文字列
    """

    __argtype__ = "str"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        argument.value = input("> ")
        return argument
