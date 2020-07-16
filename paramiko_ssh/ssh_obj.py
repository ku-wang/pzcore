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
    folder = "/root/{time}".format(time=time_str)
    ctf = "mkdir -p {folder}/c-snapshot;mkdir -p {folder}/r-snapshot".format(folder=folder)
    ssh2.run_cmd(ctf)

    locations = ["app", "snapshot", "restore"]


    def create_yaml_from_local(resource_location, target_location, ssh_obj):
        cmds = ''
        with open(resource_location) as f:
            for line in f:
                wr = line.strip('\n')
                cmd = "echo '{wr}' >> {folder};".format(wr=wr, folder=target_location)
                cmds = cmds + cmd
        ssh_obj.run_cmd(cmds)


    for loc in locations:
        if loc == "app":
            target = folder + "/c-snapshot/app.yaml"
        if loc == "snapshot":
            target = folder + "/c-snapshot/generate-snapshot-1.yaml"
        if loc == "restore":
            target = folder + "/r-snapshot/restore-snapshot-1.yaml"
        create_yaml_from_local(loc, target, ssh2)

