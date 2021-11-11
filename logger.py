from threading import Thread
from time import time
from datetime import datetime as dt
from tzlocal import get_localzone
from config import LOGPATH

utc_offset = dt.now(get_localzone()).utcoffset().total_seconds()


def encode(plain):
    cipher = []
    for num in plain:
        neg = num < 0
        num = bin(abs(num))[2:]
        while len(num) > 7:
            cipher.append('1' + num[:7])
            num = num[7:]
        cipher.append(num.rjust(8, '0'))
        cipher.append(str(int(neg)) + bin(len(num))[2:].rjust(7, '0'))
    return list(map(lambda byte: int(byte, 2), cipher))


class LogThread(Thread):
    def __init__(self, data):
        global utc_offset
        Thread.__init__(self)
        self.data = list(data) + [int((time() + utc_offset) * 1000)]

    def run(self):
        cipher = list(map(lambda n: n * 228 - 54, self.data))
        cipher = encode(cipher)
        cipher = list(map(lambda byte: (byte + 190) % 256, cipher))
        with open(LOGPATH, 'ab') as logfile:
            logfile.write(bytes(cipher))


def log(*data):
    logger = LogThread(data)
    logger.start()
    pass
