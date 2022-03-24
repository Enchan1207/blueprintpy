#!/bin/zsh
#
# クリーンアップスクリプト
#
echo "Cleaning..."

clean_count=0

function cleanup() {
    echo "Search \033[34;1m$1\033[0m ..."

    files=(`find . -path $1`)
    if [ ${#files} -eq 0 ]; then
        return 1
    fi

    for file_path in ${files[@]}; do
        echo "Removing ${file_path}"
        clean_count=$(( $clean_count + 1 ))

        rm -r $file_path
    done

    return 0
}

# __pycache__ (コンパイル済みのライブラリ)
cleanup "**/__pycache__"

# ./build (ライブラリのビルド結果)
cleanup "./build"

# *.egg-info, *.dist-info (パッケージ情報)
cleanup "**/*.egg-info"
cleanup "**/*.dist-info"

# ./dist (ビルド済みのパッケージバイナリ)
cleanup "./dist"

# 終了
echo "Cleanup finished. ${clean_count} files was removed."
exit 0
