import datetime
start_time = datetime.datetime.now()
time_str = start_time.strftime('%Y-%m-%d-%H-%M-%S')


def createfiles(ssh):

    folder = "/root/{time}".format(time=time_str)
    ctf = "mkdir -p {folder}/c-snapshot;mkdir -p {folder}/r-snapshot".format(folder=folder)
    ssh.run_cmd(ctf)

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
        create_yaml_from_local(loc, target, ssh)


if __name__ == '__main__':
    from paramiko_ssh import ssh_obj
    ip = ''
    ssh = ssh_obj.SSHObj(ip)
