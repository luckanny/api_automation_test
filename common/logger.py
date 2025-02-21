import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import os
import colorlog
from common.init_path import LOG


class Logger:
    def __init__(self, log_name="api", log_level=logging.DEBUG, max_files=5):
        """
           初始化日志类
           :param log_level: 默认日志级别
           :param log_name: 日志文件名前缀
           :param max_files: 最多保留的日志文件数
           """
        self.logger_level = log_level
        self.max_files = max_files

        # os.makedirs(os.path.dirname(self.log_file_name), exist_ok=True)
        if not os.path.exists(LOG):
            os.makedirs(LOG)

        self.log_name = LOG + os.sep + f"{log_name}_{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
        self.logger = logging.getLogger(self.log_name)

        # 设置日志格式
        self.log_format = logging.Formatter('%(asctime)s|%(levelname)8s|%(filename)10s:%(lineno)4s|%(message)s')
        # 颜色配置
        log_color = {'DEBUG': 'cyan',
                     'INFO': 'green',
                     'WARNING': 'purple',
                     'ERROR': 'red',
                     'CRITICAL': 'red,bg_white'}
        self.formatter = colorlog.ColoredFormatter(
            fmt="%(log_color)s%(asctime)s|%(levelname)8s|%(filename)10s:%(lineno)4s|%(message)s",
            log_colors=log_color
        )

    def get_logger(self):
        if not self.logger.handlers:
            # 创建串口（控制台）日志处理器
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)

            # 创建日志处理器
            handler = TimedRotatingFileHandler(self.log_name,
                                               when='midnight',
                                               interval=1,
                                               backupCount=self.max_files,
                                               delay=True,
                                               encoding='utf-8'
                                               )
            handler.setFormatter(self.log_format)

            # 配置日志
            self.logger.setLevel(self.logger_level)
            self.logger.addHandler(handler)
            self.logger.addHandler(console_handler)

        return self.logger


logger = Logger().get_logger()

