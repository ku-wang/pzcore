from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait
import time
from decorator_module import retry

# executor = ThreadPoolExecutor(max_workers=1)
# # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
# task1 = executor.submit(get_html, 3)
# task2 = executor.submit(get_html, 2)
# # done方法用于判定某个任务是否完成
# print(task1.done())
# # cancel方法用于取消某个任务,该任务没有放入线程池中才能取消成功
# print(task2.cancel())
# time.sleep(4)
# print(task1.done())
# # result方法可以获取task的执行结果
# print(task1.result())


@retry.retry(3, 5)
def for_te1st(times):
    time.sleep(1)
    print('Done With {time}'.format(time=times))

    if times == 10:
        raise Exception("eorororororor")


times = [1, 2, 3, 4, 5, 6,7,8]

client_pool = ThreadPoolExecutor(max_workers=8)
client_futures = [client_pool.submit(for_te1st, time) for time in times]
wait(client_futures, return_when=ALL_COMPLETED)
# pool = ThreadPoolExecutor(max_workers=8)
# futures = []
# for i in times:
#     futures.append(pool.submit(for_te1st, i))
# pool.shutdown()

print('main')


