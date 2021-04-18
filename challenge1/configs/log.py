import logging
from logging.handlers import TimedRotatingFileHandler as tfh
import os
import socket

hostname = socket.gethostname()
msg_seperator_type = ':::'
dt_fmt='%Y-%m-%d %H:%M:%S'
msg_fmt = "%(asctime)s {} %(levelname)s %(filename)s:%(lineno)s %(funcName)s() {} %(message)s".format(hostname, msg_seperator_type)

class loggerClass(str):
    _main_log = None

    def __new__(cls, filename=None, logLevel=None):

        if not cls._main_log:
            cls._main_log = str.__new__(cls, filename)

        return cls._main_log

    def __init__(self, filename=None, logLevel=None):
        try:
            if filename and not hasattr(self, 'logger'):
                log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                             'logs/', filename)
                try:
                    os.makedirs(os.path.dirname(log_file_path))
                except:
                    pass

                self.logger = logging.getLogger(filename)
                #self.logger.setLevel(logging.INFO)
                self.setLogLevel(logLevel)
                if not self.logger.handlers:
                    fh = tfh(log_file_path, when='midnight', interval=1, utc=True)
                    fh.setFormatter(
                        logging.Formatter(fmt=msg_fmt, datefmt=dt_fmt))
                    self.logger.addHandler(fh)

        except:
            logging.error('Logger failed', exc_info=True)
            raise

    def setLogLevel(self,logLevel=None):
        if logLevel in ( "ERROR", "error") :
            self.logger.setLevel(logging.ERROR)
        elif logLevel in ( "WARNING","warning" or "WARN" or "warn") :
            self.logger.setLevel(logging.WARNING)
        elif logLevel in ( "CRITICAL","critical") :
            self.logger.setLevel(logging.CRITICAL)
        elif logLevel in ( "DEBUG","debug") :
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)