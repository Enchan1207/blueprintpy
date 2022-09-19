#!/usr/bin/env bash
#
# バージョニングスクリプト
#

# 前処理
set -o pipefail # パイプ処理したコマンドが途中で死んだのを検知するため
OLDIFS=$IFS # IFSのリストア

# 構文は、 vercalc.sh VERSION を想定
#   VERSION : 指定するバージョン ここに与えられたバージョン文字列に従ってファイルが編集される

# -- constants -----------------------------------------------------------

# 汎用の成功/失敗
EXIT_SUCCESS=0
EXIT_FAILURE=1

# -- functions -----------------------------------------------------------

# ログを出力する. stdoutがttyでなければカラーエスケープシーケンスを除去する.
#  - Parameters:
#     - 出力内容
function log(){
    if [ -t 1 ]; then
        printf "$1\n"
    else
        printf "$1\n" | sed -r 's/\x1b\[[0-9]*(;[0-9]*)*m//g'
    fi
}

# バージョン番号を入力として受け取り、セマンティック・バージョニングに準拠しているかチェックする.
#  - Parameters:
#     - バージョン番号
#  - Returns: EXIT_(FAILURE|SUCCESS)
#  - Note: バリデーションが通った場合は入力内容をそのまま出力します. 失敗した場合は何も返しません.
function validateVersion(){
    # 変数を受け取る
    if [ $# -ne 1 ]; then
        return $EXIT_FAILURE
    fi

    OLDIFS=$IFS

    IFS=" "
    CURRENT_VERSION_STR=$1

    # メジャー、マイナー、パッチに分割
    CURRENT_VERSION=( `echo "${CURRENT_VERSION_STR}" | sed -rn 's/^v?([0-9]+)\.([0-9]+)\.([0-9]+)$/\1 \2 \3/p'` )
    [ "${#CURRENT_VERSION[*]}" -eq 3 ]; result=$?

    if [ $result -eq 0 ]; then
        echo $CURRENT_VERSION_STR
    fi

    IFS=$OLDIFS
    return $(( result ))
}

# 置換パターンとファイルパスを受け取り、バージョン情報を置き換える.
#  - Parameters:
#     - 置換パターン
#     - ファイルパス
#  - Returns: EXIT_(FAILURE|SUCCESS)
function setVersion(){
    # 変数を受け取る
    if [ $# -ne 2 ]; then
        return $EXIT_FAILURE
    fi

    # グローバルでsedが定義されていればそれを使う
    if [ -n "$SED" ]; then
        SED_="$SED"
    else
        SED_=`which sed`
    fi

    PATTERN="$1"
    FILE_PATH="$2"
    
    # ファイルがあれば
    if [ ! -e $FILE_PATH ]; then
        return 1
    fi

    # sedを実行する
    $SED_ -i "$PATTERN" "$FILE_PATH"
    return $?
}

# -- main process --------------------------------------------------------

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
