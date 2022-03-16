#
# デフォルト引数ハンドラ
#

from typing import List

from pip_init.argument import Argument
from pip_init.args_handler import ArgsHandlerBase


class DefaultArgsHandler(ArgsHandlerBase):

    @staticmethod
    def handle_args(args: List[Argument]) -> List[Argument]:
        raise NotImplementedError()
