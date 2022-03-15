#
# コンフィグシリアライザ
#
import importlib
from json.decoder import JSONDecoder
from typing import Any, Dict, Optional

from .argument import Argument
from .content import Content
from .config import Config


class ConfigSerializer:
    """テンプレート構成シリアライザ
    """

    @staticmethod
    def serialize(config: Config) -> Dict[str, Any]:
        """テンプレート構成オブジェクトをシリアライズし、結果を返します.

        Args:
            config (Config): シリアライズする構成オブジェクト

        Returns:
            Dict[str, Any]: シリアライズ結果
        """
        raise NotImplementedError()
