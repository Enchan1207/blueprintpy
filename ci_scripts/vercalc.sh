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

# 共通関数読み込み
FUNCTIONS_PATH="./ci_scripts/functions.sh"
if [ ! -e $FUNCTIONS_PATH ]; then
    printf "\033[31;1mFATAL\033[0m Failed to load common functions.\n"
    exit 1
fi
. $FUNCTIONS_PATH

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
PREFIX_COLORS=( "4" "2" "5" "3" "1" )
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
