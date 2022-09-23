#!/usr/bin/env bash
#
# バージョニングスクリプト
#

# 前処理
set -o pipefail # パイプ処理したコマンドが途中で死んだのを検知するため
OLDIFS=$IFS # IFSのリストア

# 構文は、 vercalc.sh VERSION を想定
#   VERSION : 指定するバージョン ここに与えられたバージョン文字列に従ってファイルが編集される

# 共通関数読み込み
FUNCTIONS_PATH="./ci_scripts/functions.sh"
if [ ! -e $FUNCTIONS_PATH ]; then
    printf "\033[31;1mFATAL\033[0m Failed to load common functions.\n"
    exit 1
fi
. $FUNCTIONS_PATH

# ヘルプの表示
if [ $# -ne 1 ] || [ ${1-""} = "--help" ];then

cat << EOS
Overview: auto versioning helper (Semantic-versioning compliant)

Usage: $0 VERSION

Arguments:
    VERSION     version number to set.

Example:
    $0 v2.0.0

Note:
    This script needs GNU sed. If you use BSD sed (e.g. on Darwin), please install GNU one.
EOS
    exit $EXIT_FAILURE
fi

# 使うsedコマンドを確認する.
# Darwinの場合はgsedがあるか確認し、なければこける
UNAME=`uname | tr '[:upper:]' '[:lower:]'`
if [ $UNAME = "darwin" ];then
    GSED_PATH=`which gsed`
    if [ -z $GSED_PATH ]; then
        log "\033[31mFATAL\033[0m: GNU sed won't be installed."
        exit $EXIT_FAILURE
    fi
    SED=${GSED_PATH}
else
    SED=`which sed`
fi
if [ -z $SED ]; then
    log "\033[31mFATAL\033[0m: Command sed not found."
    exit $EXIT_FAILURE
fi
log "Path to sed: ${SED}"

# 入力をバリデーション
VERSION=`validateVersion "$1"`
if [ $? -ne $EXIT_SUCCESS ]; then
    log "\033[31mFATAL\033[0m: \033[35;1m${1}\033[0m is incompliant version format."
    exit $EXIT_FAILURE
fi

log "Updating to \033[35;1m${1}\033[0m..."

# パターンとファイルを渡してバージョニング
setVersion "s/version=.*/version=${VERSION}/" ./setup.cfg
if [ $? -ne $EXIT_SUCCESS ]; then
    log "\033[31mFATAL\033[0m: Failed to update version info."
    exit $EXIT_FAILURE
fi

setVersion "s/version =.*/version = \"${VERSION}\"/" ./src/blueprintpy/core/__init__.py
if [ $? -ne $EXIT_SUCCESS ]; then
    log "\033[31mFATAL\033[0m: Failed to update version info."
    exit $EXIT_FAILURE
fi

log "Finished."
exit 0
