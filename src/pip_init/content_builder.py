#
# Content引数展開
#
from functools import reduce
from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import BaseLoader, Environment, FileSystemLoader

from .argument import Argument
from .content import Content
from .prepared_content import PreparedContent


class ContentBuilder:
    """Contentビルダー
    """

    def __init__(self,
                 template_root: str,
                 extract_root: str,
                 template_args: List[Argument],
                 template_loader: Optional[BaseLoader] = None) -> None:
        """Contentビルダーを初期化します.

        Args:
            template_root (str): 読み込むテンプレートのルート
            extract_root (str): 展開先のルート
            template_args (List[Argument]): テンプレート引数
            template_loader (Optional[BaseLoader], optional): テンプレートローダー
        """

        loader = template_loader if template_loader is not None else FileSystemLoader(template_root)
        self.env = Environment(loader=loader, trim_blocks=True)
        self.template_root = Path(template_root)
        self.extract_root = Path(extract_root)

        # テンプレート引数はdictに変換
        template_parameter_dicts: List[Dict[str, Any]] = [{arg.name: arg.value} for arg in template_args]
        self.template_args: Dict[str, Any] = reduce(lambda prev, next: prev | next, template_parameter_dicts)

    def build(self, content: Content) -> PreparedContent:
        """引数に与えられたContentオブジェクトを読み込んで処理し、展開可能なContentオブジェクトを生成します.

        Args:
            content (Content): 変換元のContent

        Returns:
            PreparedContent: 処理結果
        """

        # Content.destをf文字列展開
        formatted_dest = content.dest.format(self.template_args)

        # それぞれ絶対パスに変換
        source_abspath = self.template_root / content.src
        dest_abspath = self.extract_root / formatted_dest

        # テンプレートエンジンを通さなくてよければそのまま戻る
        if not content.use_template_engine:
            return PreparedContent(dest_abspath, source_abspath, None)

        # srcが指すファイルを読み込み、jinjaに通して返す
        template = self.env.get_template(content.src)
        render_result = template.render(self.template_args).encode()
        return PreparedContent(dest_abspath, None, render_result)
