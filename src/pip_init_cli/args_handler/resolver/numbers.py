#
# 整数・浮動小数点数
#
from pip_init import Argument

from ..exceptions import ValidationError

from .base import Resolver


class IntResolver(Resolver):
    """整数
    """

    __argtype__ = "int"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        try:
            argument.value = int(input("> "))
            return argument
        except ValueError:
            raise ValidationError(argument, f"Invalid value that cannot be processed as an integer")


class FloatResolver(Resolver):
    """浮動小数点数
    """

    __argtype__ = "float"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        try:
            argument.value = float(input("> "))
            return argument
        except ValueError:
            raise ValidationError(argument, f"Invalid value that cannot be processed as an floating point number")
