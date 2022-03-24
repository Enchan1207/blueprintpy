#
# 単純なリスト
#
"""
リスト形式のデータを代入するresolver
"""

from typing import List

from blueprintpy.core import Argument

from .base import Resolver


class ArrayResolver(Resolver):
    """__resolver_type__: :code:`array`
    """

    __resolver_type__ = "array"

    @staticmethod
    def resolve(argument: Argument) -> Argument:
        """
        リスト形式のデータについて、コンソールからの入力を元に値を生成します.
        入力するたびに内部リストに値が蓄積され、 :code:`EOF` を送信することで値が確定されます.

        Note:
            現在のバージョンでは **デフォルト値を考慮した動作をしない** ことに注意してください.
            何らかの値が必ず要求されます.
        """

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
