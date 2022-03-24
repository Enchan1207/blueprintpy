#
# 整数・浮動小数点数
#
"""
数値形式のデータを代入するresolver
"""

from blueprintpy.core import Argument

from ..exceptions import ValidationError

from .base import Resolver


class IntResolver(Resolver):
    """__resolver_type__: :code:`int`
    """

    __resolver_type__ = "int"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        """
        整数形式のデータについて、コンソールからの入力を元に値を生成します.
        """
        value = input("> ")

        if value != "":
            try:
                argument.value = int(value)
                return argument
            except ValueError:
                raise ValidationError(argument, f"Invalid value that cannot be processed as an integer")

        if argument.default_value is None:
            raise ValidationError(argument, "valid value required")

        argument.value = argument.default_value
        return argument


class FloatResolver(Resolver):
    """__resolver_type__: :code:`float`
    """

    __argtype__ = "float"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        """
        浮動小数点形式のデータについて、コンソールからの入力を元に値を生成します.
        """

        value = input("> ")

        if value != "":
            try:
                argument.value = float(value)
                return argument
            except ValueError:
                raise ValidationError(argument, f"Invalid value that cannot be processed as an integer")

        if argument.default_value is None:
            raise ValidationError(argument, "valid value required")

        argument.value = argument.default_value
        return argument
