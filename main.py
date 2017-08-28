# -*- coding: utf-8 -*-

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(["scrapy","crawl","jobbole"])
execute(["scrapy","crawl","zhihu"])
# 如果出现错误： ImportError: No module named 'win32api'
# 报错处理： pip install -i https://pypi.douban.com/simple pypiwin32