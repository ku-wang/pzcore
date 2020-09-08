import os
from decorator_module import retry
from log_module import log_m

logger = log_m.logger


@retry.retry(3, 5)
def read_l(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip())
    return lines


def read_line(filename='test1'):
    if os.path.exists(filename):
        logger.info("The {file} has existed ...")
        results = read_l(filename)
    else:
        logger.error("The {file} not exist, will create it first ...")
        f = open(filename, "w")
        f.write("write something to file")
        f.close()
        results = read_l(filename)

    return results


if __name__ == '__main__':

    with open("stat.1", "r", encoding="utf-8") as f:
        lines = f.readlines()

        with open('test_new', 'w', encoding="utf-8") as file:
            for line in lines:
                if 'Linux' in line:
                    continue
                # print(line.strip('\n'))
                old = line.strip('\n')
                if "年" in old:
                    new_year = old.split('年')[0]
                    new_month = old.split('年')[-1].split('月')[0]
                    new_day = old.split('日')[0].split('月')[-1]
                    new_hour = old.split('日 ')[-1].split('时')[0]
                    new_mins = old.split('时')[-1].split('分')[0]
                    new_s = old.split('分')[-1].split('秒')[0]
                    t = 'AM'
                    if new_hour in ['01', '03', '04', '05', '06', '07', '08', '09', '10', '11']:
                        nho = new_hour
                    elif new_hour == '00':
                        nho = '12'
                    elif new_hour == '12':
                        nho = new_hour
                        t = 'PM'
                    elif new_hour in ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']:
                        nho = str(int(new_hour) - 12)
                        if int(nho) < 10:
                            nho = '0' + nho
                        t = 'PM'
                    # print(type(new_month))
                    newnew = "{month}/{day}/{year} {hour}:{min}:{s} {t}".format(month=new_month, day=new_day, year=new_year,
                                                                         hour=nho, min=new_mins, s=new_s, t=t)
                    newnew = newnew + '\n'


                    file.write(newnew)
                else:
                    file.write(line)


