# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- PATH設定

# 拡張機能またはautodocで文書化するモジュールのパス
import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))
from blueprintpy.core import version as core_version

# -- プロジェクト情報

project = 'blueprintpy'
copyright = '2022, Enchan1207'
author = 'Enchan1207'

# alpha/beta/rcタグを含む完全なバージョン情報
release = f"v{core_version}"


# -- 一般設定

# Sphinx拡張モジュール
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_multiversion'
]

# テンプレートパス
templates_path = [
    '_templates'
]

# 言語
language = 'ja'

# 除外パターン
exclude_patterns = [
    'docs',
    'Thumbs.db',
    '.DS_Store'
]

# -- HTML出力オプション

# テーマ
html_theme = 'sphinx_rtd_theme'

# 静的ファイル配置先
html_static_path = [
    '_static'
]

# -- 拡張機能構成

# autodoc
autoclass_content = 'both'  # __init__ のdocstringを含める

html_context = {
    'display_github': True,
    'github_user': 'Enchan1207',
    'github_repo': 'blueprintpy',
    'github_version': 'release/docs/source/'
}

# sphinx-multiversion
smv_tag_whitelist = r'^v\d+\.\d+\.\d+$'  # セマンティックバージョニング
smv_branch_whitelist = r'^(release|develop)$'  # リリースブランチ、または開発ブランチ
