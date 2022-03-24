#
# 展開されるファイルコンテンツ
#

import os
from typing import Optional


class Content:
    """パッケージテンプレートに含まれるファイル.
    """

    def __init__(self,
                 src: str,
                 dest: str,
                 use_template_engine: Optional[bool] = None) -> None:
        """
        Args:
            src (str): オリジナル相対パス
            dest (str): コピー先相対パス
            use_template_engine (Optional[bool], optional): テンプレートエンジンを使用するか

        Note:
            :code:`use_template_engine` にNoneが渡された場合, 拡張子が :code:`.j2` または :code:`.jinja2` のファイルではTrue、
            それ以外のファイルではFalseがセットされます.
        """

        self.src = src
        self.dest = dest

        if use_template_engine is not None:
            self.use_template_engine = use_template_engine
        else:
            _, suffix = os.path.splitext(src)
            self.use_template_engine = suffix in ['.j2', '.jinja2']
