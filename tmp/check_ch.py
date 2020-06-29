from paramiko_ssh import ssh_obj
from log_module import log_m

logger = log_m.logger

master = '10.180.116.11'
bd_ip = '10.180.116.19'
bd_port = '10811'

ssh_obj = ssh_obj.SSHObj(master)


bd_cmd = "/usr/bin/dplmanager -m aex -a {bd_ip} -p {bd_port} devlist".format(bd_ip=bd_ip, bd_port=bd_port)

cmd1 = bd_cmd + "|grep dpl_ip|awk '{print $2}'"
cmd2 = bd_cmd + "|grep channel_uuid|awk '{print $2}'"

ips = ssh_obj.run_cmd(cmd1).strip().split('\n')
ids = ssh_obj.run_cmd(cmd2).strip().split('\n')

for ip in ips:
    for id in ids:
        cmd = "/usr/bin/dplmanager -m ch -c {id} -a {ip} -p 10809 stat detail".format(id=id, ip=ip)
        logger.info(ssh_obj.run_cmd(cmd))
        del ids[0]
        break




