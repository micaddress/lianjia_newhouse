# encoding='utf-8'
import datetime
import os
from scrapy import cmdline

table_name_end = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# start_time = '12:50:00'
start_time = '04:00:00'
print(datetime.datetime.now().strftime("%H:%M:%S") + '重新获取数据倒计时...')
while True:
    if start_time == (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(' ')[-1]):
        log_path = 'e:\\log\\lianjia_newhouse\\'
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        cmdstr = 'scrapy crawl spider_newhouse -s LOG_FILE=' + log_path + 'log_lianjia_newhouse' + table_name_end +'.txt'
        print(cmdstr)
        os.system(cmdstr)
# cmdline.execute('scrapy crawl spider_newhouse'.split())
