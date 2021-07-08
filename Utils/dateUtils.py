import datetime
import time


class DateUtils():

    def getTime(self):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    def getStartDate(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def getEndDate(self):
        d1 = datetime.datetime.now()
        d2 = d1 + datetime.timedelta(days=10)  # 增加10天
        return d2.strftime("%Y-%m-%d")