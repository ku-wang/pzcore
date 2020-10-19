#
#
# # try:
# #     xx = 1
# #     # c = 1 + 'ss'
# #
# # except Exception as e:
# #     print(e)
# #
# # else:
# #     print(xx)
#
# ip = ""
# id = ""
# idx = ""
# pvc = ""
# device = ""
#
# add = "dplmanager -m bd -a {ip} -p 10811 -s 21990232555520 -u {id} -v {pvc} --vset 1 -l {idx} -b '[]' -g 1 -j 0 " \
#       "-x '1' -d {device} add".format(ip=ip, id=id, idx=idx, pvc=pvc, device=device)
#
# print(add)
# clean_core_log_cmd = 'rm -rf /var/log/pzcl-*dpl* /var/log/pzcl-*-cdcgc-log* /var/log/pzcl-bd-vset* ' \
#                              '/var/log/pzcl-s3-vset* /var/log/pzcl-manager'
#
# print(clean_core_log_cmd)
# tmp_image = " hahdahsd"
# import datetime
#
# print(datetime.datetime.now())

for i in range(1, 11):
    print(i)