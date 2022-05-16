import multiprocessing as mp
import sys
import datetime
import time

from schedule import repeat, every, run_pending


def func(result_list):
    # 共享数值型变量
    # num.value = 2
    last_result_list = []
    # 共享数组型变量
    while True:
        for x in result_list:
            if x == '':
                flag = False
                break
        else:
            flag = True
        if flag:
            print(result_list)
            print(last_result_list)
            if eval(str(result_list)) == last_result_list:
                print('列表重复')
                time.sleep(1)
            else:
                last_result_list = eval(str(result_list))
                print('检测到新识别记录', result_list)
                time.sleep(1)


def use_num(result_list):
    # 共享数组型变量
    for x in range(1, 99):
        result_list[0] = x
        result_list[1] = datetime.datetime.now().time().microsecond
        time.sleep(5)


if __name__ == '__main__':
    # 共享数值型变量
    # num = multiprocessing.Value('d', 1)
    # print(num.value)

    # 共享数组型变量
    # num = mp.Array('i', [888])
    cross_list = mp.Manager().list()
    # 初始共享全局列表
    cross_list.append("")
    cross_list.append("")
    print('列表创建完成')

    # mp.set_start_method(method='spawn')  # init
    # queue = mp.Queue(maxsize=2)
    # processes = [mp.Process(target=image_put, args=(queue,)),
    #              mp.Process(target=image_get, args=(queue,)),
    #              mp.Process(target=image_test, args=(queue,)), ]
    processes = [mp.Process(target=func, args=(cross_list,)),
                 mp.Process(target=use_num, args=(cross_list,)),
                 ]
    try:
        for process in processes:
            process.daemon = True
            process.start()
        [process.join() for process in processes]
        while True:
            run_pending()


    except KeyboardInterrupt:
        print("mian stop...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
        sys.exit(1)
