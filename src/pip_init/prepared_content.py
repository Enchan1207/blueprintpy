#
# 展開先に書き込む準備ができたContent
#
from pathlib import Path
from typing import Optional


class PreparedContent:
    """展開可能なContent
    """

    def __init__(self,
                 dest_path: Path,
                 source: Optional[Path] = None,
                 extract_object: Optional[bytes] = None) -> None:
        """
        Args:
            dest_path (Path): 展開先の絶対パス
            source (Optional[Path], optional): 展開するファイルの絶対パス
            extract_object (Optional[bytes], optional): 展開するオブジェクトのバイト列

        Raises:
            ValueError: 展開するべきコンテンツが指定されなかった場合

        Note:
            :code:`source`, :code:`extract_object` のいずれかに有効な値が入力されている必要があります.
        """

        self.dest_path = dest_path

        if source is None and extract_object is None:
            raise ValueError("Invalid argument")

        self.source = source
        self.extract_object = extract_object
