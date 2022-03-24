#
# デフォルト引数ハンドラ
#

"""
引数ハンドラのデフォルト実装
"""

from typing import List, Optional, Type

from blueprintpy.core import Argument
from blueprintpy.cli.args_handler import ArgsHandlerBase

from .exceptions import ValidationError
from .resolver import Resolver


class DefaultArgsHandler(ArgsHandlerBase):

    """ (プロパティ :code:`__handler_name__` の値は :code:`__default__` です.)
    """

    __handler_name__ = "__default__"

    @staticmethod
    def handle_args(args: List[Argument]) -> List[Argument]:
        """
        各テンプレート引数について、プロパティ :code:`argtype` の値に対応する名称のレゾルバを探します.
        次に各レゾルバに引数オブジェクトを投入し、処理結果を プロパティ :code:`value` に代入して返します.

        対応するレゾルバが存在しない場合は :code:`RuntimeError`, レゾルバの処理が失敗した場合は :class:`.exceptions.ValidationError` が送出されます.
        """
        prepared_args: List[Argument] = []

        # 各引数について
        for arg in args:
            # 対応するresolverを探し
            argtype = arg.argtype if arg.argtype is not None else "str"
            resolver = DefaultArgsHandler.__search_resolver(argtype)
            if resolver is None:
                raise RuntimeError(f"No resolver registered that can handle argument type \033[36m{argtype}\033[0m!")

            while True:
                # 適当に名前と説明文を表示したのち
                print(f"\033[32;1m{arg.name}\033[0m ({arg.description}):")

                try:
                    # resolveして追加
                    prepared_args.append(resolver.resolve(arg))
                    break
                except ValidationError as e:
                    print(f"\033[31mError\033[0m {e.argument.name}: {e.reason}")
                    continue

        return prepared_args

    @staticmethod
    def __search_resolver(argtype: str) -> Optional[Type[Resolver]]:
        resolver_candidates = list(filter(lambda resolver: resolver.__resolver_type__ == argtype, Resolver.resolvers))
        return resolver_candidates[0] if len(resolver_candidates) == 1 else None
