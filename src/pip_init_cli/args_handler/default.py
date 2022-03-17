#
# デフォルト引数ハンドラ
#

from typing import List, Optional, Type

from pip_init import Argument
from pip_init_cli.args_handler import ArgsHandlerBase

from .exceptions import ValidationError
from .resolver import Resolver


class DefaultArgsHandler(ArgsHandlerBase):

    __handler_name__ = "__default__"

    @staticmethod
    def handle_args(args: List[Argument]) -> List[Argument]:
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
        resolver_candidates = list(filter(lambda resolver: resolver.__argtype__ == argtype, Resolver.resolvers))
        return resolver_candidates[0] if len(resolver_candidates) == 1 else None
