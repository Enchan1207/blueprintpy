#
# テンプレート構成
#

from typing import List, Optional

from .argument import Argument
from .content import Content


class Config:
    """テンプレート構成
    """

    def __init__(self,
                 name: str,
                 args: List[Argument],
                 contents: List[Content],
                 args_handler_name: Optional[str] = None) -> None:
        """テンプレート構成を初期化します.

        Args:
            name (str): テンプレート名
            args (List[Argument]): テンプレート引数リスト
            contents (List[Content]): 展開されるファイルコンテンツのリスト
            args_handler_name (Optional[str], optional): 引数ハンドラの名前
        """
        self.name = name
        self.args = args
        self.contents = contents
        self.args_handler_name = args_handler_name
