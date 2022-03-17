#
# 単純な文字列
#
from pip_init import Argument

from ..exceptions import ValidationError
from .base import Resolver


class StringResolver(Resolver):
    """単純な文字列
    """

    __argtype__ = "str"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        value = input("> ")
        if value != "":
            argument.value = value
            return argument

        if argument.default_value is None:
            raise ValidationError(argument, "valid value required")

        argument.value = argument.default_value
        return argument
