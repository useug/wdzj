import scrapy
import sched
import time
import os


class AllSpider(scrapy.Spider):
    name = 'allSpider'

    # 初始化sched模块的scheduler类
    # 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞


#初始化sched模块的scheduler类
#第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler ( time.time, time.sleep )

def perform1(inc):   #被周期性调度触发的函数
    schedule.enter(inc,0,perform1,(inc,))
    os.system("scrapy crawl wdzj_news")    # 需要周期执行的函数
def perform2(inc):   #被周期性调度触发的函数
    schedule.enter(inc,0,perform2,(inc,))
    os.system("scrapy crawl p2peye")    # 需要周期执行的函数
def perform3(inc):   #被周期性调度触发的函数
    schedule.enter(inc,0,perform3,(inc,))
    os.system("scrapy crawl wdzjhot")    # 需要周期执行的函数
def mymain():
    schedule.enter(0,0,perform1,(50,))   #每隔一天运行一次 24*60*60=86400s
    schedule.enter(0,0,perform2,(80,))   #每隔一天运行一次 24*60*60=86400s
    schedule.enter(0,0,perform3,(120,))   #每隔一天运行一次 24*60*60=86400s

if __name__=="__main__":
    mymain()
    schedule.run()  # 开始运行，直到计划时间队列变成空为止.