import re
from collections import defaultdict
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from log_module import log_m


logger = log_m.logger


class AnalyzeIOstat(object):
    """Analyze iostat output logs"""

    def __init__(self):
        super(AnalyzeIOstat, self).__init__()
        pass

    @staticmethod
    def get_datetime(pattern, line, t_start=None, t_end=None):
        """
        Get datetime from string in range t_start < datetime < e_end
        :param pattern:
        :param line:
        :param t_start:
        :param t_end:
        :return: 1: no time string matched, 2: time out of range, datetime:
        """

        t_str = re.findall(pattern, line)
        if not t_str:
            return 1

        # fmt = '%m/%d/%Y %I:%M:%S %p'  # centos:  08/12/2020 09:13:44 AM
        fmt = '%m/%d/%y %H:%M:%S'  # ubuntu:  08/12/20 19:13:44
        start_datetime = datetime.strptime(t_start, fmt) if t_start else None
        end_datetime = datetime.strptime(t_end, fmt) if t_end else None
        date_time = datetime.strptime(t_str[0], fmt)
        if start_datetime and date_time < start_datetime:
            return 2
        if end_datetime and date_time > end_datetime:
            return 3
        return date_time

    @staticmethod
    def get_key_idx(line, key_list):
        """
        Get keys index in line split
        :param line:
        :param key_list:
        :return:
        """
        logger.info("Get keys index in line split ...")
        key_idx = defaultdict(int)
        line_values = re.findall(r"\S+", line)
        for key in key_list:
            idx = line_values.index(key)
            logger.info("{0}:{1}".format(key, idx))
            key_idx[key] = line_values.index(key)
        return key_idx

    def load_data(self, data_file, device, keys=None,
                  time_start=None, time_end=None):
        """
        get device value in iostat output data

        04/16/2020 10:19:57 PM
        avg-cpu:  %user   %nice %system %iowait  %steal   %idle
                   0.50    0.00    0.17    8.28    0.00   91.05

        Device:         rrqm/s   wrqm/s     r/s     w/s    rMB/s    wMB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
        sda               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
        sdb               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
        sdc               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
        sdd               0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
        dm-0              0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
        dm-1              0.00     0.00    0.00    0.00     0.00     0.00     0.00     0.00    0.00    0.00    0.00   0.00   0.00
        ftlb              0.00     0.00    0.00    0.00     0.00     0.00     0.00    77.08    0.00    0.00    0.00   0.00 100.10

        :param data_file:
        :param device:
        :param keys: default ["r/s", "w/s"]
        :param time_start:
        :param time_end:
        :return: {"r/s":[], "w/s":[]}
        """

        logger.info("Load data from {0} ...".format(data_file))

        if keys is None:
            keys = ["r/s", "w/s"]

        # 04/16/2020 10:19:57 PM
        t_pattern = r"\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{1,2}:\d{1,2}.*\b"  # \s\S{2}
        date_time_list = []  # for plot.x
        device_kvs = defaultdict(list)  # for plot.y

        key_idx = None
        data_valid = False
        with open(data_file, "r") as f:
            lines = f.readlines()
            for line in lines:
                date_time = self.get_datetime(t_pattern, line, time_start, time_end)
                if date_time == 1:
                    pass
                elif date_time == 2:  # date_time < time start
                    data_valid = False
                elif date_time == 3:  # date_time > time end
                    break
                else:
                    data_valid = True
                    date_time_list.append(date_time)

                if not key_idx and "Device" in line:
                    key_idx = self.get_key_idx(line, keys)

                if data_valid and device in line:
                    line_values = re.findall(r"\S+", line)
                    for key in key_idx.keys():
                        device_kvs[key].append(float(line_values[key_idx[key]]))
            date_time_list = date_time_list[:len(device_kvs[keys[0]])]
        return device_kvs, date_time_list

    def show_device_iostat(self, data_file, device, keys=None,
                           time_start=None, time_end=None):
        """
        show device iostat to plot
        :param data_file:
        :param device:
        :param keys:
        :param time_start:
        :param time_end:
        :return:
        """
        logger.info("Show device iostat based on log file")
        logger.info("iostat log file: {0}".format(data_file))
        logger.info("device name: {0}".format(device))
        logger.info("keys: {0}".format(keys))
        logger.info("time_start: {0}".format(time_start))
        logger.info("time_end: {0}".format(time_end))

        device_kvs, time_list = self.load_data(
            data_file, device, keys, time_start, time_end)

        fig = plt.figure(figsize=(12, 6))
        ax1 = fig.add_subplot(1, 1, 1)
        plt.xlabel("Time(PDT)")
        plt.ylabel("IOPS")
        plt.title("bd-glusterfs-nfs, fio-rw-128k, BD Volume IOPS: iostat  -xcmdt 1")
        plt.ylim(0, 10)
        plt.gcf().autofmt_xdate()  # 自动旋转日期标记
        # 设置x轴主刻度格式
        alldays = mdates.DayLocator()  # 主刻度为每天
        ax1.xaxis.set_major_locator(alldays)  # 设置主刻度
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M:%S'))
        # 设置副刻度格式
        # hoursLoc = mpl.dates.HourLocator(interval=1)  # 为6小时为1副刻度
        mins_loc = mpl.dates.MinuteLocator(interval=20)  # 为10分钟为1副刻度
        ax1.xaxis.set_minor_locator(mins_loc)
        ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))
        # 参数pad用于设置刻度线与标签间的距离
        ax1.tick_params(pad=10)

        x = time_list
        logger.info("x len: {0}".format(len(x)))
        p_max_y = 0
        # p_len_y = 0
        # x = np.arange(0, p_len_y)
        for key in device_kvs.keys():
            y = device_kvs[key]
            max_y = max(y)
            if max_y > p_max_y:
                plt.ylim(0, max(y))
                p_max_y = max_y
            # len_y = len(y)
            # if len_y > p_len_y:
            #     x = np.arange(0, y_len)
            #     p_len_y = len_y
            label = "{0}:{1}".format(device, key)
            plt.plot(x, y, label=label, linewidth=2)

        plt.legend()
        plt.show()


if __name__ == "__main__":
    # "r/s", "w/s", "rMB/s", "wMB/s"
    iostat_output = r"C:\Users\user\Downloads\test14\log\iostat.log.1"
    dev_name = "ftlb"
    analyze_keys = ["r/s", "w/s"]
    start = None  # "04/15/2020 11:24:56 PM"
    end = None  #  "04/16/2020 04:24:56 AM"

    ai = AnalyzeIOstat()
    ai.show_device_iostat(iostat_output, dev_name, analyze_keys, start, end)
