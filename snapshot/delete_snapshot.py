from decorator_module import retry
from log_module import log_m
from paramiko_ssh import ssh_obj

logger = log_m.logger


def del_volume(ssh_obj):
    cmd = "kubectl get pvc|grep csi|awk '{print $1}'|xargs kubectl delete pvc"
    res = ssh_obj.run_cmd(cmd)
    logger.debug('\n'+res)


def del_volumesnapshot(ssh_obj):
    cmd = "kubectl get volumesnapshot|grep test|awk '{print $1}'|xargs kubectl delete volumesnapshot ;kubectl get volumesnapshotcontents.snapshot.storage.k8s.io|awk '{print $1}'|xargs kubectl delete volumesnapshotcontents.snapshot.storage.k8s.io"
    res = ssh_obj.run_cmd(cmd)
    logger.debug('\n' + res)


@retry.retry(20, 3)
def check_snapshotcotent_if_exist(ssh_obj):
    cmd = "kubectl get volumesnapshotcontents.snapshot.storage.k8s.io"

    res = ssh_obj.run_cmd(cmd)

    if not res:
        logger.debug("No snapshot content exist ...")

    else:
        logger.info(res)
        raise Exception("Still exist the snapshot content")


def del_snapshot_yaml(ssh_obj, folder):
    cmd = "cd {folder}; ls |grep shot|grep -v shot-1.yaml|xargs rm -rf".format(folder=folder)
    ssh_obj.run_cmd(cmd)


if __name__ == '__main__':

    ssh = ssh_obj.SSHObj('10.180.116.11')
    #1
    del_volume(ssh)
    del_volumesnapshot(ssh)
    # check_snapshotcotent_if_exist(ssh)

    #2
    folder1 = '/home/kwang/random/c-snapshot/'
    folder2 = '/home/kwang/random/r-snapshot/'
    del_snapshot_yaml(ssh, folder1)
    del_snapshot_yaml(ssh, folder2)

    #3
    cmd = "kubectl get po |grep -E 'csi|volume'|awk '{print $1}'|xargs kubectl delete po"
    ssh.run_cmd(cmd)
