#!/usr/bin/env bash
#
# バージョン番号計算+提案
#

# 前処理
set -o pipefail # パイプ処理したコマンドが途中で死んだのを検知するため
OLDIFS=$IFS # IFSのリストア

# 構文は、 vercalc.sh [TO] [FROM] を想定
#   TO  : コミットログの先頭のref 省略した場合はHEADとなる
#   FROM: コミットログの末端のref 省略した場合はタグ一覧の最後のものが設定される

# -- constants -----------------------------------------------------------

# 汎用の成功/失敗
EXIT_SUCCESS=0
EXIT_FAILURE=1

# バージョン比較関数で使用
IS_NEW_VERSION=0
IS_SAME_VERSION=2
IS_PREVIOUS_VERSION=3

# コミット内訳表示で使用
COMMIT_PREFIXES=( "Add" "Update" "Modify" "Delete" "Fix" )
PREFIX_COLORS=( "4" "2" "5" "3" "1" )

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
    if [ ${COMMIT_COUNTS[3]} -ge 1 ] || [ ${COMMIT_COUNTS[5]} -ge 1 ]; then
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

# -- main process --------------------------------------------------------

# ヘルプの表示
if [ $# -gt 2 ] || [ ${1-""} = "--help" ];then

cat << EOS
Overview: auto version calculator (Semantic-versioning compliant)

Usage: $0 [TO] [FROM]

Arguments:
    TO      ref of head commit. if omitted, use HEAD instead.
    FROM    ref of tail commit. if omitted, use latest tag instead.

Example:
    $0 HEAD v2.0.0

Note:
    This script assumes that commit messages are written in the following format:
        <commit_message_full> ::= [<prefix>( #<issue_number>)?] <commit_message>
        <prefix> ::= Add | Update | Modify | Delete | Release | Fix

    (SRY this isn't a perfect BNF)
    If the log contains commit messages that do not conform this, they will be ignored.

    Also, tag names must conform to semantic versioning.
EOS
    exit $EXIT_FAILURE
fi

# コミットログ分析の開始点・終了点を検索
FROM=${1-"HEAD"}
TO=${2-`searchLatestVersion`}
if [ $? -ne $EXIT_SUCCESS ]; then
    log "\033[33;1mWARNING\033[0m Semantic versioning compliant tag not found. Falling back to 0.1.0..."
    log "0.1.0"
    exit $EXIT_SUCCESS
fi
log "Analyse commit history from \033[35;1m$TO\033[0m -> \033[35;1m$FROM\033[0m ..."

# 現時点の最新バージョンを探し、バリデーション+パースしておく
IFS="."
CURRENT_VERSION=( `validateVersion "$TO" | sed 's/v//'` )
CURRENT_VERSION_STR="${CURRENT_VERSION[*]}"
if [ $? -ne $EXIT_SUCCESS ]; then
    log "\033[31;1mFATAL\033[0m Failed to parse specified version $TO."
    IFS=$OLDIFS
    exit $EXIT_FAILURE
fi
IFS=$OLDIFS

# git logからコミットメッセージの先頭部分のみを抜き出す
IFS=$'\n'
COMMIT_MESSAGES=( `git log $FROM...$TO | sed -rn 's/^    \[//p' | cut -c 1-40 | uniq` ) # uniqを挟んでいるのは、PRのマージ時にコミットメッセージがコピーされるため
IFS=$OLDIFS
if [ $? -ne $EXIT_SUCCESS ]; then
    log "\033[31;1mFATAL\033[0m Failed to get commits. Please check if you specified correct ref."
    exit $EXIT_FAILURE
fi
log "Commits: \033[;1m${#COMMIT_MESSAGES[*]}\033[0m"

# コミットのプレフィックス(Add, Update, Modify...)ごとに計数し、内訳をいい感じに表示
log "Breakdown:"
commit_counts=( 0 0 0 0 0 )
IFS=$'\n'
for i in ${!COMMIT_PREFIXES[@]}; do
    # TODO: ここもうちょっと頭良くなるはず
    count=`echo "${COMMIT_MESSAGES[*]}" | grep "^${COMMIT_PREFIXES[$i]}" | wc -l | sed 's/^ *//'`
    log "    \033[3${PREFIX_COLORS[$i]}m${COMMIT_PREFIXES[$i]}\033[0m \t${count}"
    commit_counts[$i]=$count
done
IFS=$OLDIFS

# リリースコミットを検索し、発見できた場合はバージョン番号を取り出す
IFS=$'\n'
SPECIFIED_VERSION_STR=`echo "${COMMIT_MESSAGES[*]}" | sed -rn "s/^Release.*\] (.+)$/\1/p" | head -n 1`
IFS=$OLDIFS
if [ -n "$SPECIFIED_VERSION_STR" ]; then
    log "\033[36;1mRelease commit found.\033[0m"
    
    # 次期バージョンとなりうる値かチェック isNewVersionは内部でバリデーションを行なっているのでここで何かする必要はない
    IFS="."
    SPECIFIED_VERSION="${SPECIFIED_VERSION_STR[*]}"
    isNewVersion "$CURRENT_VERSION_STR" "${SPECIFIED_VERSION}"
    result=$?
    IFS=$OLDIFS
    case $result in
    "${IS_NEW_VERSION}")
        log "Specified version \033[35;1m${SPECIFIED_VERSION}\033[0m is valid as next version.";;
    "${IS_PREVIOUS_VERSION}")
        log "\033[33;1mWARNING\033[0m Specified version \033[35;1m${SPECIFIED_VERSION}\033[0m is older than the current version. This version specification will be ignored.";;
    "${IS_SAME_VERSION}")
        log "\033[33;1mWARNING\033[0m Specified version \033[35;1m${SPECIFIED_VERSION}\033[0m is same version with current one. This version specification will be ignored.";;
    *)
        log "\033[33;1mWARNING\033[0m Validation failed: \033[35;1m${SPECIFIED_VERSION}\033[0m This version specification will be ignored.";;
    esac

    # 成功時はtailに一行表示することでパイプしやすく
    if [ $result -eq $IS_NEW_VERSION ]; then
        log "${SPECIFIED_VERSION/v/}"
        exit $EXIT_SUCCESS
    fi
fi

# 次期バージョンの増分を求める
echo "Calculate version increments..."
IFS=","
VERSION_ADDITIONS=`calcVersionAddition "${commit_counts[*]}"`
IFS=$OLDIFS
if [ $? -ne $EXIT_SUCCESS ]; then
    log "\033[31;1mFATAL\033[0m Failed to calculate version increments."
    exit $EXIT_FAILURE
fi

# 次期バージョンを求める
log "Recommended new version:"
NEW_VERSION=`getNextVersionFromAddition "$CURRENT_VERSION_STR" "$VERSION_ADDITIONS"`
if [ $? -ne $EXIT_SUCCESS ]; then
    log "\033[31;1mFATAL\033[0m Failed to parse new version."
    exit $EXIT_FAILURE
fi

# 出力して終了
log "Next version will be: \033[35;1mv${NEW_VERSION}\033[0m"
log "$NEW_VERSION"

exit 0
