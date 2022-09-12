#
# blueprintpy CLI
#
"""
blueprintpy CLIツールのメインモジュール
"""

import importlib
import sys
import logging
from argparse import ArgumentParser
from pathlib import Path
from types import ModuleType
from typing import Optional

from blueprintpy import internal_templates
from blueprintpy.core import ContentBuilder, ContentExtractor
from blueprintpy.core import version as core_version

from .args_handler import ArgsHandlerBase
from .config_loader import ConfigLoader

cli_version = "0.2.0"


def main() -> int:
    """コマンド :code:`blueprint` の実装.コマンドライン引数を処理し、テンプレート展開処理を実行します.

    Returns:
        int: 終了コード
    """
    #
    # コマンドライン引数のパース
    #

    # 引数の追加
    parser = ArgumentParser(
        prog='blueprint',
        usage="%(prog)s [target] [--name name_of_template] [--template_dir path/to/template]",
        description=f"Generic package configuration CLI generator",

        epilog=f"Internal templates are placed and will be searched at: {Path(internal_templates.__file__).parent}")
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
    parser.add_argument(
        "--verbose", "-v",
        action='store_true',
        help="show verbose output",
        default=False)
    parser.add_argument(
        "--version",
        action="version",
        help="show version information and exit",
        version=f"blueprintpy core v{core_version}, cli v{cli_version}"
    )

    # パースして情報を取得
    args = parser.parse_args()
    extract_root: Path = Path(args.target).absolute()
    template_name: str = args.name
    additional_template_dir: Optional[Path] = Path(args.template_dir).absolute() if args.template_dir is not None else None
    is_dry_run = args.dry_run
    is_verbose = args.verbose

    #
    # ロギング構成
    #
    log_handler = logging.StreamHandler(stream=sys.stdout)
    if is_verbose:
        log_handler.setLevel(logging.INFO)
    else:
        log_handler.setLevel(logging.WARNING)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)

    #
    # メイン処理
    #

    logger.info(f"blueprintpy core v{core_version}, cli v{cli_version}")

    if is_dry_run:
        logger.warning("\033[;1mDry-run Mode enabled\033[0m")

    # template_rootが指定された場合は絶対パスに変換し、sys.pathに追加しておく
    if additional_template_dir is not None:
        logger.info(f"Additional directory specified: {str(additional_template_dir)}")
        sys.path.append(str(additional_template_dir))
    # そうでなければ ~/.blueprintpy/をsys.pathに追加する
    # このディレクトリは存在してもしなくてもよい
    else:
        sys.path.append(str(Path.home() / ".blueprintpy"))

    # パスを解決し、テンプレートをimportする
    # blueprintpy.internal_templates、blueprintpy_templatesでそれぞれ該当する名前のテンプレートを探す
    logger.info("Find and import templates...")
    template_module: Optional[ModuleType] = None
    try:
        template_module = importlib.import_module(f"blueprintpy.internal_templates.{template_name}")
    except ImportError:
        logger.warning(f"Template \033[36m{template_name}\033[0m not found at inrernal template. found custom template directory...")

    # どちらにもなければエラー
    if template_module is None:
        try:
            template_module = importlib.import_module(f"blueprintpy_templates.{template_name}")
        except ImportError:
            logger.error("\033[31;1mFailed to import template. check if the path is valid.\033[0m")
            logger.error(f"search path: \033[36mblueprintpy_templates.{template_name}\033[0m")
            return 1
    logger.info(f"Template module resolved at: {template_module.__file__}")

    # importしたモジュールからテンプレートの親ディレクトリを特定し、template.jsonを読み込む
    template_root = Path(template_module.__file__).parent
    with open(template_root / "template.json") as f:
        template_json = f.read()
    config = ConfigLoader.load(template_json)
    logger.info(f"Template configuration \033[36m{config.name}\033[0m loaded.")

    # 引数ハンドラを特定する
    args_handler_name = config.args_handler_name or "__default__"
    logger.info(f"Resolve argument handler \033[36m{args_handler_name}\033[0m...")
    args_handler_candidates = list(filter(lambda handler: handler.__handler_name__ == args_handler_name, ArgsHandlerBase.handlers))
    logger.info(f"Candidates: {','.join(map(str, args_handler_candidates))}")
    if len(args_handler_candidates) != 1:
        logger.error("\033[31;1mCould not identify argument handler.\033[0m")
        return 1
    args_handler = args_handler_candidates[0]
    logger.info(f"Argument handler \033[36m{args_handler.__handler_name__}\033[0m resolved.")

    # 引数ハンドラに渡して値をセットしてもらう
    prepared_args = args_handler.handle_args(config.args)
    logger.info(f"{len(prepared_args)} Arguments are handled.")

    # Contentをビルド
    logger.info(f"Build contents...")
    content_builder = ContentBuilder(template_root, extract_root, prepared_args)
    prepared_contents = [content_builder.build(content) for content in config.contents]

    # 配置先ディレクトリが空でなかったら警告を表示
    if not is_dry_run and (len(list(extract_root.iterdir())) != 0):
        logger.warning("\033[33mWARNING:extract destination (specified at [target] operand) includes files or directories.")
        logger.warning("Continue? [yN]\033[0m")

        if input().lower() != "y":
            print("Aborted.")
            return 0

    # 配置
    logger.info(f"Extracting...")
    for content in prepared_contents:
        logger.info(f"extract: {content.source} -> {content.dest_path}")

        if not is_dry_run:
            ContentExtractor.extract(content)

    # 完了
    print("Succeeded.")
    return 0
