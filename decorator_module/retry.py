import time
import random
from log_module import log_m

logger = log_m.log_obj()


def retry(retry_times=3, wait_time=10):
    def decoration_2(func):
        def decoration_1(*args, **kwargs):
            for _retry in range(1, retry_times+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if _retry == retry_times:
                        logger.error("{error}, retry times arrived !({tries} / {total_tries})".format(error=e, tries=_retry, total_tries=retry_times))
                        raise e
                    else:
                        logger.error('{error}, after {time}s will retry ! ({t} / {total})'.format(error=e, time=wait_time, t=_retry, total=retry_times))
                        time.sleep(wait_time)

        return decoration_1
    return decoration_2


@retry(3, 5)
def for_test():
    r_number = random.randint(0, 100)
    if r_number < 50:
        raise Exception("The random number is lower than 50 ...")
    else:
        logger.info('No way, i pass it')
