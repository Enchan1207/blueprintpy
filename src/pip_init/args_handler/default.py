#
#
#

from typing import List

from ..argument import Argument
from .base import ArgsHandlerBase


class DefaultArgsHandler(ArgsHandlerBase):

    @staticmethod
    def handle_args(args: List[Argument]) -> List[Argument]:
        pass
