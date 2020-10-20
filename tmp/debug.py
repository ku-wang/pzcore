# #
# #
# # # try:
# # #     xx = 1
# # #     # c = 1 + 'ss'
# # #
# # # except Exception as e:
# # #     print(e)
# # #
# # # else:
# # #     print(xx)
# #
# # ip = ""
# # id = ""
# # idx = ""
# # pvc = ""
# # device = ""
# #
# # add = "dplmanager -m bd -a {ip} -p 10811 -s 21990232555520 -u {id} -v {pvc} --vset 1 -l {idx} -b '[]' -g 1 -j 0 " \
# #       "-x '1' -d {device} add".format(ip=ip, id=id, idx=idx, pvc=pvc, device=device)
# #
# # print(add)
# # clean_core_log_cmd = 'rm -rf /var/log/pzcl-*dpl* /var/log/pzcl-*-cdcgc-log* /var/log/pzcl-bd-vset* ' \
# #                              '/var/log/pzcl-s3-vset* /var/log/pzcl-manager'
# #
# # print(clean_core_log_cmd)
# # tmp_image = " hahdahsd"
# # import datetime
# #
# # print(datetime.datetime.now())
#
# for i in range(1, 11):
#     print(i)

# files_num = 10
# mount_point = "/var/lib/kubelet/pods/7160a953-d941-404b-b96d-254cd83bc0f6/volumes/kubernetes.io~csi/vbos-ff1976ac-9f77-4d92-b883-81c166d1fa9c/mount"
# folder = "test"
# max = 5
# min = 1
#
# cmd = "for i in {l}1..{num}{r};do time dd if=/dev/urandom of={mount_point}/{for_test}/$i.txt " \
#           "count=$((RANDOM%{max}+{min})) bs=1MB;echo sleep 2;sleep 2;echo '';done".format(num=files_num, mount_point=mount_point,
#             for_test=folder, l="{", r="}", max=max, min=min)
#
# print(cmd)
import random, datetime, copy

templat = {"_id": 0, "loc": '', "name": '', "date": '', "company": "EVI"}
locs = ["Shot_Guard", "Point_Guard", "Center", "Small_Forward", "Power_Forward"]
nums = 10
templates = []
for num in range(1, nums):
    template = copy.deepcopy(templat)
    template['_id'] = num
    template['loc'] = random.choice(locs)
    # template['name'] = mongo_data.generate_random_string(6)
    template['date'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    print(template)
    templates.append(template)

print(templates)