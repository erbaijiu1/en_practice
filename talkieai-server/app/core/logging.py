import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 设置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='[File: %(filename)s, Line: %(lineno)d]:%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

