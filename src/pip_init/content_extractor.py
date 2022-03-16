#
# Contentを適切な場所に配置する
#

from shutil import copyfile

from .prepared_content import PreparedContent


class ContentExtractor:
    """PreparedContentを適切な場所に展開する
    """

    @staticmethod
    def extract(content: PreparedContent):
        """引数に渡されたパラメータ展開済みのコンテンツを適切な場所に配置します.

        Args:
            content (PreparedContent): 配置するコンテンツ

        Raises:
            ValueError: コンテンツのパスが不正であるか、コンテンツの指すオブジェクトが不正だった場合

        Note:
            コンテンツの各パスは絶対パスである必要があります.
            また、Extractorは与えられたコンテンツのパスを検証しないことに注意してください.
            (パスのバリデーションは引数ハンドリングプロセスで行うことを推奨します)
        """

        # 読み込み元、配置先が絶対パスであることを確認する
        if not content.dest_path.is_absolute():
            raise ValueError("Invalid argument")
        if content.source is not None and not content.source.is_absolute():
            raise ValueError("Invalid argument")

        # 書き込み
        if content.source is not None:
            copyfile(content.source, content.dest_path)
        elif content.extract_object is not None:
            with open(content.dest_path, "wb") as f:
                f.write(content.extract_object)
        else:
            raise ValueError("Invalid argument")