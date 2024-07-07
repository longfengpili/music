# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2024-07-07 09:52:49
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2024-07-07 14:02:06

from .conf import LOGGING_CONFIG
import logging.config
logging.config.dictConfig(LOGGING_CONFIG)
