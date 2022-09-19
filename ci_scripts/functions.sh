#!/usr/bin/env bash
#
# CIスクリプト共通関数
#

# 前処理
set -o pipefail # パイプ処理したコマンドが途中で死んだのを検知するため

# -- constants -----------------------------------------------------------

# 汎用の成功/失敗
EXIT_SUCCESS=0
EXIT_FAILURE=1

# バージョン比較関数で使用
IS_NEW_VERSION=0
IS_SAME_VERSION=2
IS_PREVIOUS_VERSION=3

# バージョン番号計算に使用
COMMIT_PREFIXES=( "Add" "Update" "Modify" "Delete" "Fix" )

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

# セマンティック・バージョニングに基づき、バージョン間の差異を計算する.
#  - Parameters:
#     - 現在のバージョン
#     - 次のバージョン
#  - Returns: (IS_NEW_VERSION|IS_SAME_VERSION|IS_PREVIOUS_VERSION|EXIT_FAILURE)
#  - Note: 関数内でバージョンのバリデーションを行なっておりますので、前処理は必要ありません.
function isNewVersion(){
    # 変数を受け取る
    if [ $# -ne 2 ]; then
        return $EXIT_FAILURE
    fi

    # バリデーション
    CURRENT_VERSION_STR=`validateVersion "$1"`
    if [ $? -ne 0 ]; then
        return $EXIT_FAILURE
    fi
    NEW_VERSION_STR=`validateVersion "$2"`
    if [ $? -ne 0 ]; then
        return $EXIT_FAILURE
    fi

    OLDIFS=$IFS

    # バージョン文字列を配列にパース
    IFS="."
    CURRENT_VERSION=( ${CURRENT_VERSION_STR/v/} )
    NEW_VERSION=( ${NEW_VERSION_STR/v/} )
    IFS=$OLDIFS

    # メジャー、マイナー、パッチの順に、
    # 新しいバージョンとされる方が値が大きければ新バージョン、そうでなければ旧バージョンとする
    for i in ${!NEW_VERSION[@]}; do
        if [ ${NEW_VERSION[$i]} -gt ${CURRENT_VERSION[$i]} ];then
            return $IS_NEW_VERSION
        elif [ ${NEW_VERSION[$i]} -lt ${CURRENT_VERSION[$i]} ];then
            return $IS_PREVIOUS_VERSION
        fi
    done

    # ここに落ちてくるのは完全に同じ値が入った時
    return $IS_SAME_VERSION
}

# コミット履歴から最新リリースのバージョンを検索する.
#  - Returns: EXIT_(FAILURE|SUCCESS)
#  - Note: git tagコマンドは現在のブランチからまっすぐ辿れるタグ以外も表示してしまうので、
#          単一のブランチ(master,releaseなど)からタグを付加している前提です.
function searchLatestVersion(){
    OLDIFS=$IFS

    # git tagの出力をリバースし、
    IFS=$'\n'
    TAGS=( `git tag | tac` )
    IFS=$OLDIFS

    # 最初にバリデーションが通った時点のものを採用する
    for tag in ${TAGS[@]}; do
        validateVersion $tag
        if [ $? -eq 0 ]; then
            return $EXIT_SUCCESS
        fi
    done
    return $EXIT_FAILURE
}

# プレフィックス別に計数されたコミット数から、次期バージョンの増分を計算する.
#  - Parameters:
#     - プレフィックス別コミット数 ($COMMIT_PREFIXESの順に従いカンマ区切りで列挙)
#  - Returns: EXIT_(FAILURE|SUCCESS)
#  - Note: 増分結果は major,minor,patchの形式で標準出力されます.
function calcVersionAddition(){
    # 変数を受け取る
    if [ $# -ne 1 ]; then
        return $EXIT_FAILURE
    fi

    OLDIFS=$IFS

    IFS=","
    COMMIT_COUNTS=( $1 )
    IFS=$OLDIFS

    # 要素数はあっているか?
    if [ ${#COMMIT_COUNTS[*]} -ne $(( ${#COMMIT_PREFIXES[*]} )) ]; then
        return $EXIT_FAILURE
    fi

    version_addition=(0 0 0)

    # メジャーバージョンアップ要因:
    #   - 現状なし ただし、増加処理を行えるようにしておく
    version_addition[0]=0

    # マイナーバージョンアップ要因:
    #   - Updateコミットが1以上
    if [ ${COMMIT_COUNTS[1]} -ge 1 ]; then
        version_addition[1]=1
    fi

    # パッチバージョンアップ要因:
    #   - Fix, Modifyコミットが1以上
    if [ ${COMMIT_COUNTS[3]} -ge 1 ] || [ ${COMMIT_COUNTS[4]} -ge 1 ]; then
        version_addition[2]=1
    fi

    IFS=","
    echo "${version_addition[*]}"
    IFS=$OLDIFS
    return $EXIT_SUCCESS
}

# バージョン増分と現在のバージョン値から、次期バージョンを計算する.
#  - Parameters:
#     - 現在のバージョン
#     - バージョン増分 (major,minor,patchの順にカンマ区切りで列挙)
#  - Returns: EXIT_(FAILURE|SUCCESS)
#  - Note: 次期バージョンはセマンティック・バージョニングに従い標準出力されます.
function getNextVersionFromAddition(){
    # 変数を受け取る
    if [ $# -ne 2 ]; then
        return $EXIT_FAILURE
    fi

    OLDIFS=$IFS

    # バージョンのバリデーションとパース
    IFS="."
    CURRENT_VERSION=( `validateVersion "$1" | sed 's/v//'` )
    if [ $? -ne $EXIT_SUCCESS ]; then
        IFS=$OLDIFS
        exit $EXIT_FAILURE
    fi
    IFS=$OLDIFS

    # バージョン増分の取得
    IFS=","
    VERSION_ADDITIONS=( $2 )
    IFS=$OLDIFS

    # 要素数はあっているか?
    if [ ${#VERSION_ADDITIONS[*]} -ne 3 ]; then
        return $EXIT_FAILURE
    fi

    # 新バージョンの計算
    # TODO ここもっと頭良くなるはず
    NEW_VERSION=( ${CURRENT_VERSION[*]} )
    if [ ${VERSION_ADDITIONS[0]} -eq 1 ]; then
        NEW_VERSION[0]=$(( ${CURRENT_VERSION[0]}+1 ))
        NEW_VERSION[1]=0
        NEW_VERSION[2]=0
    elif [ ${VERSION_ADDITIONS[1]} -eq 1 ]; then
        NEW_VERSION[1]=$(( ${CURRENT_VERSION[1]}+1 ))
        NEW_VERSION[2]=0
    elif [ ${VERSION_ADDITIONS[2]} -eq 1 ]; then
        NEW_VERSION[2]=$(( ${CURRENT_VERSION[2]}+1 ))
    fi

    IFS="."
    echo "${NEW_VERSION[*]}"
    IFS=$OLDIFS
    return $EXIT_SUCCESS
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
