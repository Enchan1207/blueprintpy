#
# テンプレート構成
#

from typing import List

from .args_handler import ArgsHandlerBase

from .argument import Argument
from .content import Content


class Config:
    """テンプレート構成
    """

    def __init__(self,
                 name: str,
                 args: List[Argument],
                 contents: List[Content],
                 args_handler: ArgsHandlerBase) -> None:
        """テンプレート構成を初期化します.

        Args:
            name (str): テンプレート名
            args (List[Argument]): テンプレート引数リスト
            contents (List[Content]): 展開されるファイルコンテンツのリスト
        """
