from decorator_module import retry
from log_module import log_m
from paramiko_ssh import ssh_obj

logger = log_m.logger


def del_volume(ssh_obj):
    cmd = "kubectl get pvc|grep csi|awk '{print $1}'|xargs kubectl delete pvc"
    res = ssh_obj.run_cmd(cmd)
    logger.debug('\n'+res)


def del_volumesnapshot(ssh_obj):
    cmd = "kubectl get volumesnapshot|grep test|awk '{print $1}'|xargs kubectl delete volumesnapshot"
    res = ssh_obj.run_cmd(cmd)
    logger.debug('\n' + res)


@retry.retry(3, 3)
def check_snapshotcotent_if_exist(ssh_obj):
    cmd = "kubectl get volumesnapshotcontents.snapshot.storage.k8s.io"

    res = ssh_obj.run_cmd(cmd)

    if not res:
        logger.debug("No snapshot content exist ...")

    else:
        logger.info(res)
        raise Exception("Still exist the snapshot content")


if __name__ == '__main__':

    ssh = ssh_obj.SSHObj('10.180.116.11')
    check_snapshotcotent_if_exist(ssh)
