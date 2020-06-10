from paramiko_ssh import ssh_obj

master = '10.180.116.11'
bd_ip = '10.180.116.17'
bd_port = '10811'

ssh_obj = ssh_obj.SSHObj(master)


bd_cmd = "/usr/bin/dplmanager -m aex -a {bd_ip} -p {bd_port} devlist".format(bd_ip=bd_ip, bd_port=bd_port)

cc = ssh_obj.run_cmd(bd_cmd)
print(cc)
ips_ids = {}

