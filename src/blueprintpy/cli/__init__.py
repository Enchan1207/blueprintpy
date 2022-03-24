#
# blueprintpy CLI
#

"""
blueprintpy CLIツール
"""

from .cli import main


def blueprint() -> int:
    """
    コマンド :code:`blueprint` を提供する関数. KeyboardInterrupt (:code:`^C`) のみがこの関数でハンドルされ,
    それ以外の処理は 関数 :func:`.cli.main` が担当しています.

    Returns:
        int: 終了コード
    """

    try:
        return main()
    except KeyboardInterrupt:
        print("\n")
        print("\033[31;1mProcess aborted by user interaction.\033[0m")
        print("\n")
        return 1
