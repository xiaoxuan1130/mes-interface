import time


class DateUtils():

    def getTime(self):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
