import testlink, time
from test_link.conf.testlink_settings import *

manual = 1  # manual
automation = 2  # automation
# import ssl


class Testlink_obj(object):
    _tl_obj = None

    def __init__(self, url, dev_key):
        self.url = url
        self.key = dev_key
        if self._tl_obj is None:
            self._tl_obj = testlink.TestlinkAPIClient(self.url, self.key)

    def get_test_project(self):
        projects = self._tl_obj.getProjects()

        projects_info = []
        for project in projects:
            projects_info.append({"project_id": project["id"], "project_name": project["name"]})

        return projects_info

    # get test plan, validated
    def get_test_plan(self, project_id):
        test_plans = self._tl_obj.getProjectTestPlans(project_id)
        plans_info = []
        for test_plan in test_plans:
            plans_info.append({"plan_id": test_plan["id"], "plan_name": test_plan["name"]})

        return plans_info

    # get test suite, validated
    def get_test_suites_by_test_plan(self, test_plan_id):
        test_suites = self._tl_obj.getTestSuitesForTestPlan(test_plan_id)

        test_suites_info = []
        for test_suite in test_suites:
            test_suites_info.append({"test_suite_id": test_suite["id"], "test_suite_name": test_suite["name"]})

        return test_suites_info

    # get test case, validated
    def get_test_cases_by_test_suite(self, test_suite_id):
        test_cases = self._tl_obj.getTestCasesForTestSuite(test_suite_id, True, None)

        test_cases_info = []
        for test_case in test_cases:
            if test_case:
                test_cases_info.append({"test_case_id": test_case["id"], "test_case_name": test_case['name'],
                                    "case_infact_id": test_case['external_id']})

        return test_cases_info

    # get test suite, validated
    def get_test_suite(self):
        projects = self._tl_obj.getProjects()
        top_suites = self._tl_obj.getFirstLevelTestSuitesForTestProject(projects[0]["id"])
        for suite in top_suites:
            print("test suite", suite["id"], suite["name"])

    # create test suite, validated
    def create_test_suite(self, project_id="1", test_suite_name="test02", test_suite_describe="test01",
                          father_id=""):
        if father_id == "":
            self._tl_obj.createTestSuite(project_id, test_suite_name, test_suite_describe)
        else:
            self._tl_obj.createTestSuite(project_id, test_suite_name, test_suite_describe, parentid=father_id)

    # create test case, Unverified
    def create_test_case(self, father_id, data):
        self._tl_obj.initStep(data[0][2], data[0][3], automation)
        for i in range(1, len(data)):
            self._tl_obj.appendStep(data[i][2], data[i][3], automation)
        self._tl_obj.createTestCase(data[0][0], father_id, "1", "timen.xu", "", preconditions=data[0][1])

    # get test case, Unverified
    def get_test_case(self, test_case_id):
        test_case = self._tl_obj.getTestCase(testcaseid=test_case_id)
        cases = []
        for step in test_case:
            for m in step.get("steps"):
                cases.append({"序列": m.get("step_number"), "执行步骤": m.get('actions').strip('\n').strip('</p>'),
                              "预期结果": m.get('expected_results').strip('\n').strip('</p>')})
        return cases

    # report test result, validated
    def report_test_result(self, test_plan_id, test_case_id, final_test_result, test_notes, execduration,
                           platform_name, build_name):
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self._tl_obj.reportTCResult(testcaseid=test_case_id, testplanid=test_plan_id, status=final_test_result,
                                   guess=True, testcaseexternalid=None, platformname=platform_name,
                                   buildname=build_name, execduration=execduration,
                                   timestamp=localtime, steps=[], notes=test_notes)

    def get_result(self, test_plan_id, test_case_id):
        response = self._tl_obj.getLastExecutionResult(testplanid=test_plan_id, testcaseid=test_case_id)
        print("getAllExecutionsResults", response)
        return response

    def get_total_for_test_plan(self, test_plan_id):
        response = self._tl_obj.getTotalsForTestPlan(testplanid=test_plan_id)
        print("getTotalsForTestPlan", response)
        return response

    def get_builds_for_test_plan(self, test_plan_id):
        response = self._tl_obj.getBuildsForTestPlan(testplanid=test_plan_id)
        print("getBuildsForTestPlan", response)
        return response

    def get_exec_counter_by_build(self, test_plan_id):
        response = self._tl_obj.getExecCountersByBuild(testplanid=test_plan_id)
        print("getExecCountersByBuild", response)
        return response

    def get_test_suites_for_test_plan(self, test_plan_id):
        response = self._tl_obj.getTestSuitesForTestPlan(test_plan_id)
        print("getTestSuitesForTestPlan", response)
        return response

    def get_test_cases_for_test_plan(self, test_plan_id, build_id, platform_id, execstatus):
        if execstatus == 'p' or execstatus == 'f' or execstatus == 'b':
            response = self._tl_obj.getTestCasesForTestPlan(testplanid=test_plan_id, buildid=build_id,
                                                           platformid=platform_id, executestatus=execstatus)
            print("getTestCasesForTestPlan A  ", response)
            return response
        elif execstatus == 'n':
            response = self._tl_obj.getTestCasesForTestPlan(testplanid=test_plan_id, buildid=build_id,
                                                           platformid=platform_id)
            print("getTestCasesForTestPlan A  ", response)
            return response

    def get_test_case_assigned_tester(self, test_plan_id, build_id, platform_id, testcase_id):
        response = self._tl_obj.getTestCaseAssignedTester(testplanid=test_plan_id, buildid=build_id,
                                                         platformid=platform_id, testcaseexternalid=testcase_id)
        print("getTestCasesForTestPlan A  ", response)
        return response


if __name__ == '__main__':

    tl_obj = Testlink_obj(TestLink_url, private_key)

    # 获取所有project 的 id ,name
    project_info = tl_obj.get_test_project()

    # 获取目标 id
    for project in project_info:
        if project['project_name'] == 'EasyStack':
            project_id = project['project_id']
            break

    # 通过 project id 来获取 test plan
    plans_info = tl_obj.get_test_plan(project_id)

    for plan in plans_info:
        if plan['plan_name'] == 'Regression Testing':
            plan_id = plan['plan_id']

    # 通过 plan id 来获取 用例集
    suite_info = tl_obj.get_test_suites_by_test_plan(plan_id)

    for suite in suite_info:
        if suite['test_suite_name'] == "特殊场景":
            suite_id = suite['test_suite_id']

    cases_info = tl_obj.get_test_cases_by_test_suite(suite_id)

    for case in cases_info:
        if case['case_infact_id'] == "ECS-8210":
            case_id = case['test_case_id']
            break

    target_case_info = tl_obj.get_test_case(case_id)
    print(target_case_info)

