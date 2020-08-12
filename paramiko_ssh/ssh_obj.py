# coding:utf-8
import paramiko
from decorator_module import retry
from log_module import log_m
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait


import datetime
start_time = datetime.datetime.now()
time_str = start_time.strftime('%Y-%m-%d-%H-%M-%S')

logger = log_m.log_obj("ssh-"+time_str+'.log', logger_name="SSH")


class SSHObj(object):
    _ssh_obj = None

    def __init__(self, ip, port=22, username='root', pwd='password'):
        self.ip = ip
        self.port = port
        self.username = username
        self.pwd = pwd

    def connect(self):
        logger.debug("Connect to {ip}".format(ip=self.ip))
        ssh_obj = paramiko.SSHClient()
        ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_obj.connect(hostname=self.ip, port=self.port, username=self.username, password=self.pwd)

        self._ssh_obj = ssh_obj

        return self._ssh_obj

    def close(self):
        self._ssh_obj.close()

    def run_cmd(self, cmd):
        logger.debug('Run the {cmd} via {ip}'.format(cmd=cmd, ip=self.ip))
        stdin, stdout, stderr = self.connect().exec_command(cmd)

        results = str(stdout.read(), encoding='utf-8')
        self.close()
        return results

if __name__ == '__main__':
    # # initial the ssh
    node1 = "10.180.116.11"
    # ssh1 = SSHObj(ip='10.199.128.100')
    ssh2 = SSHObj(node1)
    #
    # # create the tmp folder on env


