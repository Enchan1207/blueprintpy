blueprintpy
###########

.. image:: https://raw.githubusercontent.com/Enchan1207/blueprintpy/master/banner.png
    :target: https://github.com/Enchan1207/blueprintpy/actions/workflows/ci.yml
    :alt: banner



.. image:: https://github.com/Enchan1207/blueprintpy/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/Enchan1207/blueprintpy/actions/workflows/ci.yml
    :alt: Unittest status


.. image::  https://img.shields.io/github/v/release/Enchan1207/blueprintpy
    :alt: version info

|　

Overview
========

**blueprintpy** は、Pythonに :code:`npm init` や :code:`swift init` のようなパッケージ構成CLIを提供するユーティリティです。

pip用に最適化されたテンプレートがデフォルトで用意されていますが、自分好みの構成をゼロから作成することも可能です。
また展開処理には `Jinja2 <https://jinja.palletsprojects.com/en/3.0.x/>`_ を採用しているため、Pythonパッケージ以外の用途にも使用できます。

テンプレートはPythonモジュールとして読み込まれるので、必要に応じてCLIの動作をカスタマイズすることも可能です。

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
