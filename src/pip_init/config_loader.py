#
# テンプレートjsonローダ
#

from .models import Config


class ConfigLoader:
    """テンプレート構成ファイルのローダー
    """

    @staticmethod
    def load(config_json_str: str) -> Config:
        """構成ファイルからテンプレートコンフィグを生成します.

        Args:
            config_json_str (str): 構成ファイルの内容

        Raises:
            ValueError: 不正な値が渡された場合.

        Returns:
            Config: 生成結果
        """
        raise NotImplementedError()
