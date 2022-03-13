#
# 展開されるファイルコンテンツ
#

class Content:
    """展開されるファイルコンテンツ
    """

    def __init__(self,
                 src: str,
                 dest: str) -> None:
        """ファイルコンテンツを初期化します.

        Args:
            src (str): オリジナル相対パス
            dest (str): コピー先相対パス
        """
