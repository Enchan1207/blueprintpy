#
# blueprintpy CLI
#
"""
blueprintpy CLIツールのメインモジュール
"""

import importlib
import sys
from argparse import ArgumentParser
from pathlib import Path
from types import ModuleType
from typing import Optional

from blueprintpy.core import ContentBuilder, ContentExtractor

from .args_handler import ArgsHandlerBase
from .config_loader import ConfigLoader


def main() -> int:
    """コマンド :code:`blueprint` の実装.コマンドライン引数を処理し、テンプレート展開処理を実行します.

    Returns:
        int: 終了コード
    """
    # コマンドライン引数の設定
    parser = ArgumentParser(
        prog='blueprint',
        usage="%(prog)s [target] [--name name_of_template] [--template_dir path/to/template]",
        description="Python package template extractor")
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="template extract destination (Defaults to current directory)")
    parser.add_argument(
        "--name", "-n",
        default="default",
        help="name of template (Defaults to library internal template \"default\")")
    parser.add_argument(
        "--template_dir", "-t",
        help="template root directory (optional)")
    parser.add_argument(
        "--dry_run", "-d",
        action='store_true',
        help="shows only which files are expanded")

    # パースして情報を取得
    args = parser.parse_args()
    extract_root: Path = Path(args.target).absolute()
    template_name: str = args.name
    additional_template_dir: Optional[Path] = Path(args.template_dir).absolute() if args.template_dir is not None else None
    is_dry_run = args.dry_run

    if is_dry_run:
        print("Execute as dry-run mode.")

    # template_rootが指定された場合はsys.pathに追加しておく
    if additional_template_dir is not None:
        sys.path.append(str(additional_template_dir))
    # そうでなければ ~/.blueprintpy/をsys.pathに追加する
    # このディレクトリは存在してもしなくてもよい
    else:
        sys.path.append(str(Path.home() / ".blueprintpy"))

    # パスを解決し、テンプレートをimportする
    # blueprintpy.internal_templates、blueprintpy_templatesでそれぞれ該当する名前のテンプレートを探す
    template_module: Optional[ModuleType] = None
    try:
        template_module = importlib.import_module(f"blueprintpy.internal_templates.{template_name}")
    except ImportError:
        print(f"template \033[36m{template_name}\033[0m not found at inrernal template. found custom template directory...")

    # どちらにもなければエラー
    if template_module is None:
        try:
            template_module = importlib.import_module(f"blueprintpy_templates.{template_name}")
        except ImportError:
            print("\033[31;1mfailed to import template! check if the path is valid.\033[0m")
            print(f"search path: \033[36mblueprintpy_templates.{template_name}\033[0m")
            return 1

    # importしたモジュールからテンプレートの親ディレクトリを特定し、template.jsonを読み込む
    template_root = Path(template_module.__file__).parent
    with open(template_root / "template.json") as f:
        template_json = f.read()
    config = ConfigLoader.load(template_json)

    # 引数ハンドラを特定する
    args_handler_name = config.args_handler_name or "__default__"
    args_handler_candidates = list(filter(lambda handler: handler.__handler_name__ == args_handler_name, ArgsHandlerBase.handlers))
    if len(args_handler_candidates) != 1:
        print("\033[31;1mcould not identify argument handler!\033[0m")
        return 1
    args_handler = args_handler_candidates[0]

    # 引数ハンドラに渡して値をセットしてもらう
    prepared_args = args_handler.handle_args(config.args)

    # Contentをビルド
    content_builder = ContentBuilder(template_root, extract_root, prepared_args)
    prepared_contents = [content_builder.build(content) for content in config.contents]

    # 配置
    for content in prepared_contents:
        if not is_dry_run:
            ContentExtractor.extract(content)
        else:
            print(f"expand: {content.source} -> {content.dest_path}")

    # 完了
    print("Succeeded.")
    return 0


if __name__ == "__main__":
    result = 0
    try:
        result = main() or 0
    except KeyboardInterrupt:
        print("Ctrl+C")
        exit(result)
