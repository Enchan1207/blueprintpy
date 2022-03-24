#
# テンプレート構成
#

from typing import List, Optional

from .argument import Argument
from .content import Content


class Config:
    """パッケージテンプレートの構成.
    """

    def __init__(self,
                 name: str,
                 args: List[Argument],
                 contents: List[Content],
                 args_handler_name: Optional[str] = None) -> None:
        """
        Args:
            name (str): テンプレート名
            args (List[Argument]): テンプレート引数リスト
            contents (List[Content]): 展開されるファイルコンテンツのリスト
            args_handler_name (Optional[str], optional): 引数ハンドラの名前

        Note:
            :code:`args_handler_name` パラメータには、引数ハンドラ(:mod:`blueprintpy.cli.args_handler`)の
            属性 :code:`__handler_name__` の値を指定してください.
            指定がなかった場合は、blueprintpy.cliが自動でデフォルトのハンドラを呼び出します.
        """
        self.name = name
        self.args = args
        self.contents = contents
        self.args_handler_name = args_handler_name
