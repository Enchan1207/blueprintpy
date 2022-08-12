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
    """Contentビルダ
    """

    def __init__(self,
                 template_root: Path,
                 extract_root: Path,
                 template_args: List[Argument],
                 template_loader: Optional[BaseLoader] = None) -> None:
        """
        Args:
            template_root (Path): 読み込むテンプレートのルート
            extract_root (Path): 展開先のルート
            template_args (List[Argument]): テンプレート引数
            template_loader (Optional[BaseLoader], optional): テンプレートローダー

        Note:
            :code:`template_root` , :code:`extract_root` は、インスタンス初期化時に絶対パスに変換されます.
        """

        loader = template_loader if template_loader is not None else FileSystemLoader(template_root)
        self.env = Environment(loader=loader, trim_blocks=True)
        self.template_root = template_root.absolute()
        self.extract_root = extract_root.absolute()

        # テンプレート引数はdictに変換
        template_parameter_dicts: List[Dict[str, Any]] = [{arg.name: arg.value} for arg in template_args]
        if len(template_parameter_dicts) == 0:
            # (functools.reduceは空っぽのシーケンスに使うと怒られる)
            self.template_args: Dict[str, Any] = {}
            return

        self.template_args = reduce(lambda prev, next: prev | next, template_parameter_dicts)

    def build(self, content: Content) -> PreparedContent:
        """引数に与えられたContentオブジェクトを読み込んで処理し、展開可能なContentオブジェクトを生成します.

        Args:
            content (Content): 変換元のContent

        Returns:
            PreparedContent: 処理結果
        """

        # Content.destをjinjaに通し、配置先の絶対パスを生成
        dest_template = Environment(loader=BaseLoader()).from_string(content.dest)
        formatted_dest = dest_template.render(self.template_args)
        dest_abspath = self.extract_root / formatted_dest

        # テンプレートエンジンを通さなくてよければそのまま戻る
        if not content.use_template_engine:
            source_abspath = self.template_root / content.src
            return PreparedContent(dest_abspath, source_abspath, None)

        # srcが指すファイルを読み込み、jinjaに通して返す
        content_template = self.env.get_template(content.src)
        render_result = content_template.render(self.template_args).encode()
        return PreparedContent(dest_abspath, None, render_result)
