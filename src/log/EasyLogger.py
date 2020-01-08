#!/usr/local/python/bin
# coding=utf-8

'''Implements a simple log library.
 
This module is a simple encapsulation of logging module to provide a more
convenient interface to write log. The log will both print to stdout and
write to log file. It provides a more flexible way to set the log actions,
and also very simple. See examples showed below:
 
Example 1: Use default settings
 
    import log
 
    log.debug('hello, world')
    log.info('hello, world')
    log.error('hello, world')
    log.critical('hello, world')
 
Result:
Print all log messages to file, and only print log whose level is greater
than ERROR to stdout. The log file is located in '/tmp/xxx.log' if the module 
name is xxx.py. The default log file handler is size-rotated, if the log 
file's size is greater than 20M, then it will be rotated.
 
Example 2: Use set_log to change settings
 
    # Change limit size in bytes of default rotating action
    log.set_log(limit = 10240) # 10M
 
    # Use time-rotated file handler, each day has a different log file, see
    # logging.handlers.TimedRotatingFileHandler for more help about 'when'
    log.set_log(when = 'D', limit = 1)
 
    # Use normal file handler (not rotated)
    log.set_log(backup_count = 0)
 
    # File log level set to INFO, and stdout log level set to DEBUG
    log.set_log(level = 'DEBUG:INFO')
 
    # Both log level set to INFO
    log.set_log(level = 'INFO')
 
    # Change default log file name and log mode
    log.set_log(filename = 'yyy.log', mode = 'w')
 
    # Change default log formatter
    log.set_log(fmt = '[%(levelname)s] %(message)s'
'''
 
__author__ = "astralrovers"
__status__ = "Development"
 
__all__ = ["elog", 'set_log', 'debug', 'info', 'warning', 'error',
           'critical', 'exception']
 
import os
import sys
import logging
import logging.handlers
 
# Color escape string
COLOR_RED='\033[1;31m'
COLOR_GREEN='\033[1;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[1;34m'
COLOR_PURPLE='\033[1;35m'
COLOR_CYAN='\033[1;36m'
COLOR_GRAY='\033[1;37m'
COLOR_WHITE='\033[1;38m'
COLOR_RESET='\033[1;0m'
 
# Define log color
LOG_COLORS = {
    'DEBUG': '%s',
    'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
    'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
    'ERROR': COLOR_RED + '%s' + COLOR_RESET,
    'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
    'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
}
 
elog = None
_date_form = '%Y-%m-%d %H:%M:%S'

class NoLog:

    def __init__(self):
        pass

    def debug(self, log):
        pass    

    def info(self, log):
        pass 

    def warning(self, log):
        pass 

    def error(self, log):
        pass 

    def critical(self, log):
        pass 

    def exception(self, log):
        pass 


class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''
 
    def __init__(self, fmt = None, datefmt = None):
        logging.Formatter.__init__(self, fmt, datefmt)
 
    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
 
        return LOG_COLORS.get(level_name, '%s') % msg
 

def import_log_funcs():
    '''Import the common log functions from the global logger to the module.'''
 
    curr_mod = sys.modules[__name__]
    log_funcs = ['debug', 'info', 'warning', 'error', 'critical',
                 'exception']

    for func_name in log_funcs:
        func = getattr(elog, func_name)
        setattr(curr_mod, func_name, func)


def add_handler(cls, level, fmt, colorful, **kwargs):
    '''Add a configured handler to the global logger.'''
 
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.DEBUG)
 
    handler = cls(**kwargs)
    handler.setLevel(level)
 
    if colorful:
        formatter = ColoredFormatter(fmt, _date_form)
    else:
        formatter = logging.Formatter(fmt, _date_form)
 
    handler.setFormatter(formatter)
    elog.addHandler(handler)
 
    return handler


def add_streamhandler(level, fmt):
    '''Add a stream handler to the global logger.'''
    return add_handler(logging.StreamHandler, level, fmt, True)
 

def add_filehandler(level, fmt, filename , mode, backup_count, limit, when):
    '''Add a file handler to the global logger.'''
    kwargs = {}
 
    kwargs['filename'] = filename
 
    # Choose the filehandler based on the passed arguments
    if backup_count == 0: # Use FileHandler
        cls = logging.FileHandler
        kwargs['mode' ] = mode
    elif when is None:  # Use RotatingFileHandler
        cls = logging.handlers.RotatingFileHandler
        kwargs['maxBytes'] = limit
        kwargs['backupCount'] = backup_count
        kwargs['mode' ] = mode
    else: # Use TimedRotatingFileHandler
        cls = logging.handlers.TimedRotatingFileHandler
        kwargs['when'] = when
        kwargs['interval'] = limit
        kwargs['backupCount'] = backup_count
 
    return add_handler(cls, level, fmt, False, **kwargs)


def set_log(filename=None, mode='a', level='DEBUG:INFO',
               fmt='[%(asctime)s][%(levelname)s][%(filename)s %(funcName)s %(lineno)d]: %(message)s',
               backup_count=5, limit=20480, when=None):
    '''Configure the global logger.'''

    level = level.split(':')
 
    if len(level) == 1: # Both set to the same level
        s_level = f_level = level[0]
    else:
        s_level = level[0]  # StreamHandler log level
        f_level = level[1]  # FileHandler log level
 
    add_streamhandler(s_level, fmt)

    # 有文件路径时日志才写文件
    if filename:

        logdir = '/'.join(filename.split('/')[:-1])
        # 创建文件夹
        if os.path.isfile(logdir) or not os.path.exists(logdir): 
            os.mkdir(logdir)

        add_filehandler(f_level, fmt, filename, mode, backup_count, limit, when)
 
    # Import the common log functions for convenient
    import_log_funcs()


# 初始化日志管理器
elog = logging.getLogger()

# 默认等级
elog.setLevel(logging.DEBUG)

# 基本设置
set_log()

def _test():
    elog.debug('hello, world')
    elog.info('hello, world')
    elog.error('hello, world')
    elog.critical('hello, world')

if __name__ == "__main__":
    # Set a default logger
    _test()
