#
# 単純なリスト
#
from typing import List
from .base import Resolver
from pip_init import Argument


class ArrayResolver(Resolver):
    """単純なリスト
    """
    __argtype__ = "array"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        value_buffer: List[str] = []
        print("Entered 'list mode'. ^D (Ctrl+D) to exit.")
        while True:
            try:
                value = input("> ")
            except EOFError:
                print()
                break

            if value != "":
                value_buffer.append(value)

            print(f"Current: {','.join(value_buffer)}")

        argument.value = value_buffer
        return argument
