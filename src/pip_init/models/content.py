#
# テンプレートコンテンツ
#

class Content:
    """テンプレートコンテンツ
    """

    def __init__(self, source_path: str, dest_path: str) -> None:
        """テンプレートコンテンツを生成します.

        Args:
            source_path (str): コンテンツのベースとなるファイルのパス
            dest_path (str): コンテンツ配置先の相対パス
        """
        self.source_path = source_path
        self.dest_path = dest_path
