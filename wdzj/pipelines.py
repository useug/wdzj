import time
import pymysql
from scrapy.conf import settings



# wdzj_platform_exposure----yr
class WdzjPipeline(object):
    host = settings['MYSQL_HOST']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DBNAME']
    c = settings['utf8']
    port = settings['MYSQL_PORT']
    client = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    cur = client.cursor()

    def process_item(self, item, spider):
        datas = item['datas']
        all_data = self.query_data()
        list_top_old = self.is_top()

        if len(all_data) == 0:  # 表中无数据
            print("表中无数据")
            self.insert_all(datas)
            print("全部插入完成")
        else:
            print("表中有数据")
            print(all_data)
            print (len(all_data))
            dictTitle = {}
            list_top = []
            for i in range(len(all_data)):   #数据库中type=1的数据title放入dictTitle
                tit = all_data[i][1]
                dictTitle[tit] = "tt"

            for data in datas:
                title = data['title']
                is_top = data['is_top']
                if is_top == 1:
                    list_top.append(title)  # 存放datas中所有is_top= 1 的数据
                else:
                    pass
                if title in dictTitle:
                    print("数据已存在,跳过")
                    continue
                else:
                    self.insert_data(data)
                    dictTitle[title] = "tt"
                    print("插入一条数据")

            self.compare_is_top(list_top_old, list_top)

    def insert_all(self, datas):
        sql = "INSERT INTO wdzj_and_p2peye_news(title,source,exposure_time,url,is_top,create_user_id,type,is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        for data in datas:
            lis = (data['title'], data['source'], data['exposure_time'], data['url'], data['is_top'], 1, 1, 1)
            self.cur.execute(sql, lis)
            self.client.commit()

    # 查询wdzj_and_p2peye_news 中type=1的所有数据
    def query_data(self):
        sql = "select * from wdzj_and_p2peye_news w where w.type='%s'" % (1)
        self.cur.execute(sql)
        return self.cur.fetchall()

    def is_top(self):
        list_top = []
        sql = "select * from wdzj_and_p2peye_news w where w.type='%s' and w.is_top='%s' " % (1, 1)
        self.cur.execute(sql)
        datas = self.cur.fetchall()
        lens = len(datas)
        if lens > 0:
            for i in range(lens):
                title = datas[i][1]
                list_top.append(title)
        else:
            pass
        return list_top

    def insert_data(self, data):
        sql = "INSERT INTO wdzj_and_p2peye_news(title,source,exposure_time,url,is_top,create_user_id,type,is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        lis = (data['title'], data['source'], data['exposure_time'], data['url'], data['is_top'], 1, 1, 1)
        self.cur.execute(sql, lis)
        self.client.commit()

    def  compare_is_top(self,list_top_old, list_top):
        list = []
        if len(list_top_old) > 0:
            for i in range(len(list_top_old)):
                temp = list_top_old[i]
                if temp not in list_top:
                    list.append(temp)

        if len(list) > 0:
            sql = 'UPDATE wdzj_and_p2peye_news w SET w.is_top = 0 WHERE w.title in (%s) ' % ','.join(['%s'] * len(list))
            self.cur.execute(sql,list)
            self.client.commit()
        if len(list_top) > 0:
            sql = 'UPDATE wdzj_and_p2peye_news w SET w.is_top = 1 WHERE w.title in (%s) ' % ','.join(['%s'] * len(list_top))
            self.cur.execute(sql, list_top)
            self.client.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.client.close()


#wdzj_exposure----flx
class ExposurePipeline(object):
    host = settings['MYSQL_HOST']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DBNAME']
    c = settings['utf8']
    port = settings['MYSQL_PORT']
    client = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c,port=port)
    cur = client.cursor()
    temp = []

    def process_item(self, item, spider):
        datas = item['datas']
        if self.query_data():#表中无数据
            print("表中无数据")
            self.insert_all(datas)
            print("全部插入完成")
        else:
            print("表中有数据")
            self.query_all_title()#查询数据库中所有title数据并存入list中
            self.update_all_top()#更新数据所有置顶为未置顶
            for data in datas:
                title =data['title']
                #数据是否存在库中
                if title in self.temp:
                    #数据是否需要置顶
                    if data['stick'] == '1':
                        self.update_top(title)
                        print("数据已存在，需要置顶")
                    else:
                        print("数据已存在并且未置顶,跳过")
                        continue
                else:
                    self.insert_data(data)
                    self.temp.append(title)
                    print("插入一条数据")


    def insert_all(self,datas):
        sql = 'insert into wdzj_and_p2peye_news(title,type,url,insert_time,create_user_id,is_deleted) VALUES (%s,%s,%s,%s,%s,%s)'
        for data in datas:
            lis = (data['title'],'4', data['url'],time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())),'1','0')
            self.cur.execute(sql, lis)
            self.client.commit()

    def query_data(self):
        sql = "select count(*) from wdzj_and_p2peye_news where type = '4'"
        sum = self.cur.execute(sql)
        if sum != 0 :
            return False
        else:
            return True

    def query_all_title(self):
        sql = "select title from wdzj_and_p2peye_news where type = '4'"
        self.cur.execute(sql)
        results = self.cur.fetchall()
        for result in results:
            self.temp.append(result[0])

    def insert_data(self,data):
        sql = 'insert into wdzj_and_p2peye_news(title,type,url,insert_time,create_user_id,is_deleted,is_top) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        lis = (data['title'],'4', data['url'],
               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), '1', '0',data['stick'])
        self.cur.execute(sql, lis)
        self.client.commit()

    #更新数据是否置顶
    def update_top(self,title):
        sql = "UPDATE wdzj_and_p2peye_news SET is_top = '1' where title = '%s'"%(title)
        self.cur.execute(sql)
        self.client.commit()

    #把所有数据更新为未置顶
    def update_all_top(self):
        sql = "UPDATE wdzj_and_p2peye_news SET is_top = '0' where type = '4'"
        self.cur.execute(sql)
        self.client.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.client.close()

#wdzj_hot----tym
class WdzjHotPipeline(object):
    # 连接数据库
    host = settings['MYSQL_HOST']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DBNAME']
    c = settings['utf8']
    port = settings['MYSQL_PORT']
    client = pymysql.connect(host=host, port=port, user=user, passwd=psd, db=db,
                             charset=c, cursorclass=pymysql.cursors.DictCursor, use_unicode=True)
    # 使用cursor()方法创建一个游标对象
    cur = client.cursor()

    def process_item(self, item, spider):
        datas = item['datas']
        if self.query_data():  # 表中无数据
            print("表中无数据")
            self.insert_all(datas)
            print("全部插入完成")
        else:
            print("表中有数据")
            for data in datas:
                title = data['title']
                if self.query_title(title):
                    self.insert_data(data)
                    print("插入一条数据")
                else:
                    print("数据已存在,跳过")
                    continue

    def insert_all(self, datas):
        sql = 'insert into wdzj_and_p2peye_news(title,source,exposure_time,type,url,insert_time,create_user_id,is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        for data in datas:
            lis = (
                data['title'], data['source'], data['exposure_time'], '3', data['url'],
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), '1', '0')
            self.cur.execute(sql, lis)
            self.client.commit()

    def query_data(self):
        sql = 'select count(*) from wdzj_and_p2peye_news'
        sum = self.cur.execute(sql)
        if sum != 0:
            return False
        else:
            return True

    def query_title(self, title):
        sql = "select * from wdzj_and_p2peye_news where title='%s'" % (title)
        result = self.cur.execute(sql)
        if result == 0:
            return True
        else:
            return False

    def insert_data(self, data):
        sql = 'insert into wdzj_and_p2peye_news(title,source,exposure_time,type,url,insert_time,create_user_id,is_deleted) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        lis = (
            data['title'], data['source'], data['exposure_time'], '3', data['url'],
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), '1', '0')
        self.cur.execute(sql, lis)
        self.client.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.client.close()
    # sql = 'insert into wdzj_newslist(news_subMessage,news_source,news_time,news_title) VALUES (%s,%s,%s,%s)'
    # lis = (item['news_subMessage'], item['news_source'], item['news_time'], item['news_title'])
