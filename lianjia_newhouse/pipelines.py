# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time,pymysql,requests,json,datetime

class LianjiaNewhousePipeline(object):
    def __init__(self):
        params = {
            'host' : '127.0.0.1',
            # 'host' : '192.168.2.199',
            'user' : 'root',
            'password' : 'zh850113',
            'database' : 'michael_lianjia_newhouse',
            'port' : 3306,
            'charset' : 'utf8'
        }
        self.count = 0
        self.conn = pymysql.connect(**params)
        self.cursor = self.conn.cursor()
        # self.cursor.execute("show tables")
        # self.table_name_tuple = self.cursor.fetchall()
        # self.table_name_list = []
        # for table_name in self.table_name_tuple:
        #     self.table_name_list.append(table_name[0])


    def open_spider(self,spider):
        print('爬虫开始...')
        self.start_time = time.time()
        self.start_timestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.table_name_end = '_'+datetime.datetime.now().strftime("%Y_%m_%d")
        self.create_table_tag = True


    def process_item(self, item, spider):
        province = ''
        city = 'hefei'
        # province = item['province']
        # city = item['city']
        # tb = ''
        # for py in pypinyin.pinyin(self.tb_name, style=pypinyin.NORMAL):
        #     tb+=''.join(py)
        # if tb_name not in self.table_name_list:
        #     self.create_table(tb_name)
        tb_name = province + city + self.table_name_end
        if self.create_table_tag:
            self.create_table(tb_name)
            self.create_table_tag = False
        sql_to_table_newhouse = '''insert into ''' + tb_name + '''(
                                                                    province,
                                                                     city,
                                                                    t_sales,
                                                                    a_sales,
                                                                    a_name,
                                                                    name,
                                                                    price,
                                                                    danwei,
                                                                    address,
                                                                    page_url,
                                                                    detail_url,
                                                                    record_time
                                                                    ) values (%s,%s,%s,%s,%s,
                                                                              %s,%s,%s,%s,%s,
                                                                              %s,%s)'''
        a = self.cursor.execute(sql_to_table_newhouse, (
                                                      item['province'],
                                                     item['city'],
                                                     item['total_sales'],
                                                     item['area_sales'],
                                                     item['area_name'],
                                                     item['xiaoqu_name'],
                                                     item['xiaoqu_price'],
                                                     item['price_danwei'],
                                                     item['xiaoqu_address'],
                                                     item['page_url'],
                                                     item['detail_url'],
                                                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print(a)
        self.conn.commit()
        return item

    def close_spider(self,spider):
        try:
            print('*' * 50, '开始于 ', self.start_timestr, '*' * 50)
            print('*' * 50, '结束于 ', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'       ', '*' * 50)
            self.cost_time()
            print(spider.access_city_list)
        except Exception as e:
            print('出错了')
            raise e
        finally:
            self.conn.commit()
            self.conn.close()

    def cost_time(self):
        cost_time = time.time() - self.start_time
        cost_hour = str(cost_time / 3600).split('.')[0]
        cost_min_second = (cost_time - float(cost_hour) * 3600)
        cost_min = str(cost_min_second / 60).split('.')[0]
        cost_second = str(cost_min_second - float(cost_min) * 60).split('.')[0]
        cost_hour = int(cost_hour)
        cost_min = int(cost_min)
        cost_second = int(cost_second)
        if cost_hour == 0 and cost_min == 0 and cost_second > 0:
            print('...爬虫结束，耗时 : ', cost_second, '秒！！！')
        elif cost_hour == 0 and cost_min > 0 and cost_second == 0:
            print('...爬虫结束，耗时 : ', cost_min, '分钟！！！')
        elif cost_hour > 0 and cost_min == 0 and cost_second == 0:
            print('...爬虫结束，耗时 : ', cost_hour, '小时！！！')
        elif cost_hour == 0 and cost_min > 0 and cost_second > 0:
            print('...爬虫结束，耗时 : ', cost_min, '分', cost_second, '秒！！！')
        elif cost_hour > 0 and cost_min == 0 and cost_second > 0:
            print('...爬虫结束，耗时 : ', cost_hour, '小时 零', cost_second, '秒！！！')
        elif cost_hour > 0 and cost_min > 0 and cost_second == 0:
            print('...爬虫结束，耗时 : ', cost_hour, '小时', cost_min, '分钟！！！')
        elif cost_hour > 0 and cost_min > 0 and cost_second > 0:
            print('...爬虫结束，耗时 : ', cost_hour, '小时', cost_min, '分', cost_second, '秒！！！')

    def create_table(self,tb_name):
        create_SQL = 'DROP TABLE IF EXISTS ' + tb_name + ';'
        self.cursor.execute(create_SQL)
        self.cursor.execute('''CREATE TABLE ''' + tb_name + '''  (
                                                id int(11) NOT NULL AUTO_INCREMENT,
                                                record_time datetime(0) NULL DEFAULT NULL,
                                                province varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                city varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                t_sales int(11) NULL DEFAULT NULL,
                                                a_name varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                a_sales int(11) NULL DEFAULT NULL,
                                                name varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                price varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                danwei varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                address varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                page_url varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                detail_url varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                                                PRIMARY KEY (id) USING BTREE
                                                ) ENGINE = MyISAM CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
                                ''')
        # self.cursor.execute('TRUNCATE TABLE ' + tb_name + ';')
        # self.table_name_list.append(tb_name)