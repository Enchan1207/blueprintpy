blueprintpy
===========

.. image:: https://raw.githubusercontent.com/Enchan1207/blueprintpy/HEAD/banner.png
    :alt: banner

|ImageLink|

.. |ImageLink| image:: https://img.shields.io/pypi/v/blueprintpy
.. _ImageLink: https://pypi.org/project/blueprintpy/

Overview
========

**blueprintpy** は、:code:`npm init` や :code:`swift init` のようなパッケージ構成CLIを生成するユーティリティです。

パッケージ構成は Jinja2を使用したテンプレートで管理され、自由に作成・カスタマイズできます。
デフォルトではpypi準拠のPythonパッケージおよびCMake準拠のC++プロジェクト用CLIが用意されていますが、
今後の更新によって随時追加していく予定です。 もちろん、ユーザの皆様からのPRも歓迎です。

Installation
============

blueprintpyはPyPIで公開されています。パッケージとともにCLIツール :code:`blueprint` がインストールされます。

::

    pip install blueprintpy

Indices
=======

.. toctree::
   :maxdepth: 1

   easy_usage
   use_custom_template
   package_reference
