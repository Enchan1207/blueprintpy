#
# Contentを適切な場所に配置する
#

from shutil import copyfile

from .prepared_content import PreparedContent


class ContentExtractor:
    """PreparedContentの展開
    """

    @staticmethod
    def extract(content: PreparedContent):
        """引数に渡されたPreparedContentを適切な場所に配置します.

        Args:
            content (PreparedContent): 配置するコンテンツ

        Raises:
            ValueError: コンテンツのパスが不正であるか、コンテンツの指すオブジェクトが不正だった場合

        Note:
            コンテンツの各パスは絶対パスである必要があります.

            また、:code:`content` のパスは検証されません.
            内容のバリデーションは引数ハンドリングプロセスで行うことを推奨します.
        """

        # 読み込み元、配置先が絶対パスであることを確認する
        if not content.dest_path.is_absolute():
            raise ValueError("Invalid argument")
        if content.source is not None and not content.source.is_absolute():
            raise ValueError("Invalid argument")

        # 書き込み先パスに到達できるよう、親ディレクトリまでは作成しておく
        content.dest_path.parent.mkdir(parents=True, exist_ok=True)

        # 書き込み
        if content.source is not None:
            copyfile(content.source, content.dest_path)
        elif content.extract_object is not None:
            with open(content.dest_path, "wb") as f:
                f.write(content.extract_object)
        else:
            raise ValueError("Invalid argument")
