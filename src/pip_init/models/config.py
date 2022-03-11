#
# テンプレートコンフィグ
#

from typing import List, Optional

from ..arg_handler import ArgumentHandlerBase
from . import Argument, Content


class Config:
    """テンプレート(template.json)情報の保持・管理
    """

    def __init__(self,
                 name: str,
                 args: List[Argument],
                 contents: List[Content],
                 arg_handler: Optional[ArgumentHandlerBase] = None) -> None:
        """引数に与えられた情報をもとにテンプレート構成を生成します。

        Args:
            name (str): テンプレート名
            args (List[Argument]): テンプレート要求引数
            contents (List[Content]): コンテンツ
            arg_handler (Optional[ArgumentHandlerBase]): 引数ハンドラ
        """
        self.name = name
        self.args = args
        self.contents = contents
        self.arg_handler = arg_handler
