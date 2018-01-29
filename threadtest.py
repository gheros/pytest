# import threading
# from time import ctime,sleep
#
#
# def music(func):
#         print ("I was listening to %s. %s" %(func,ctime()))
#
# def move(func):
#     i=0
#     while i<100:
#         print ("I was at the %s! %s" %(func,ctime()))
#         sleep(5)
#         i=i+1
#
# threads = []
# t1 = threading.Thread(target=music,args=(u'爱情买卖',))
# threads.append(t1)
# t2 = threading.Thread(target=move,args=(u'阿凡达',))
# threads.append(t2)
#
# if __name__ == '__main__':
#     for t in threads:
#         t.setDaemon(True)
#         t.start()
#         t.start
#
#     print ("all over %s" %ctime())

from time import sleep, ctime
import threading

loops = [4, 2]


def loop(nloop, nsec):
    print('start loop', nloop, 'at:', ctime())
    sleep(nsec)
    print('loop', nloop, 'done at:', ctime())


def main():
    print('starting at:', ctime())
    threads = []
    nloops = range(len(loops))
    print(nloops)
    # 创建线程
    for i in nloops:
        print(i)
        print(loops[i])
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)
    # 开始线程

    for i in nloops:
        threads[i].start()
    # 等待所有结束线程
    for i in nloops:
        threads[i].join()
    print('all end:', ctime())


if __name__ == '__main__':
    main()