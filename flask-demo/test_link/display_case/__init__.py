from test_link import cases

# from prettytable import PrettyTable
from test_link.conf.testlink_settings import *

tl_obj = cases.Testlink_obj(TestLink_url, private_key)
# table = PrettyTable(["Number", "Actions", "Expect_Results"])


def display_case():
    return tl_obj.get_test_case('83932')



# for step in display_case():
#     table.add_row([step['序列'], step['执行步骤'], step['预期结果']])


if __name__ == '__main__':
    # j = ''/
    # for i in display_case():
    #     j += i
    # print(j)
    print(type(display_case()))