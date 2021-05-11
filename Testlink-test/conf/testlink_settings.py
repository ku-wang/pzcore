TestLink_url = "https://testlink.easystack.cn/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
private_key = "459533000ba735458ec5beb9628451b0"

stack_project = {
    "project_name": "EasyStack",
    'project_id': '2'
}

stack_plans = {
    'Regression Testing': {
        'id': '6',
        'name': 'Regression Testing',
        'notes': '用于追踪产品回归测试',
        'active': '1',
        'is_public': '1',
        'testproject_id': '2'
    },

    'Self Testing': {
        'id': '24',
        'name': 'Self Testing',
        'notes': '自测测试计划，用于追踪开发自测的执行',
        'active': '1',
        'is_public': '1',
        'testproject_id': '2'
    },

    'System Testing': {
        'id': '25',
        'name': 'System Testing',
        'notes': '<p>用于追踪系统测试（端到端测试）</p>',
        'active': '0',
        'is_public': '1',
        'testproject_id': '2'
    },

    'Stability/Reliability': {
        'id': '10',
        'name': 'Stability/Reliability',
        'notes': '<p>该测试计划涵盖了openstack各组件，数据库，消息队列和存储的稳定性和可靠性测试，包含一定压力下，部分模块受损时的系统稳定性</p>',
        'active': '0',
        'is_public': '1',
        'testproject_id': '2'
    }

    }

flask_demo = "https://www.jianshu.com/p/e3a975ed1449"