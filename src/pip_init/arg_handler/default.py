#
# デフォルト引数ハンドラ
#

from typing import List
from . import ArgumentHandlerBase
from ..models import Argument


class DefaultArgumentHandler(ArgumentHandlerBase):
    """デフォルト引数ハンドラ
    """

    @staticmethod
    def handle_args(args: List[Argument]) -> List[Argument]:
        # TODO: コンソールから値を取得して代入して返すだけ
        raise NotImplementedError()
