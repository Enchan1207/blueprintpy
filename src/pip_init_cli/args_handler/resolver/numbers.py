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
    """浮動小数点数
    """

    __argtype__ = "float"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
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
