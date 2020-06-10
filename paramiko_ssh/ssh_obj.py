# coding:utf-8
import paramiko
from decorator_module import retry
from log_module import log_m

logger = log_m.logger


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


# ssh = SSHObj(ip='10.180.116.11')
#
# cc = ssh.run_cmd('ls')
# print(cc)
