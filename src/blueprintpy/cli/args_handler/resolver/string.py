#
# 単純な文字列
#
"""
文字列形式のデータを代入するresolver
"""

from blueprintpy.core import Argument

from ..exceptions import ValidationError
from .base import Resolver


class StringResolver(Resolver):
    """__resolver_type__: :code:`str`
    """

    __resolver_type__ = "str"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        """
        文字列形式のデータについて、コンソールからの入力を元に値を生成します.
        """

        value = input("> ")
        if value != "":
            argument.value = value
            return argument

        if argument.default_value is None:
            raise ValidationError(argument, "valid value required")

        argument.value = argument.default_value
        return argument
