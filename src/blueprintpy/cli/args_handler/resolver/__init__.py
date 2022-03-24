#
# 引数レゾルバ
#

"""
テンプレート引数 (:mod:`blueprintpy.core.argument` に格納する値を解決・代入するパッケージ.

インタフェース :class:`.Resolver` を基底クラスとし、カスタムテンプレート内で拡張することができます.
"""

from . import numbers, string, lists
from .base import Resolver as Resolver
