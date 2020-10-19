from pymongo import MongoClient
import mongo.mongo_data_tmp as mongo_data
import random
import datetime

# template of data -> for test
template = {"_id": 0, "loc": '', "name": '', "date": '', "company": "EVI"}
locs = ["Shot_Guard", "Point_Guard", "Center", "Small_Forward", "Power_Forward"]
ip = '10.180.116.17'
port = 30515
database_for_test = "chris_wang"
cl_for_test = "NBA" + str(random.randint(199999, 999999))

# -------------------------------


class Mongo():

    _client = None

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        if self._client is None:
            self._client = MongoClient("mongodb://{ip}:{port}/".format(ip=self.ip, port=self.port))

    def list_all_databases(self):
        return self._client.list_database_names()

    def get_db_connection(self, db_name):
        return self._client[db_name]

    def get_collection_obj(self, db_obj, connection_name):
        return db_obj[connection_name]

    def list_all_collections(self, db_connection):
        return db_connection.list_collection_names()

    def insert_data_by_collection(self, collection_obj, nums):
        templates = []
        for num in range(1, nums):
            template['_id'] = num
            template['loc'] = random.choice(locs)
            template['name'] = mongo_data.generate_random_string(6)
            template['date'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            templates.append(template)

        collection_obj.insert_many(templates)


def run(ip, port, db_name, collection_name, nums=10):
    mongo_obj = Mongo(ip, port)

    db_obj = mongo_obj.get_db_connection(db_name)
    collection_obj = mongo_obj.get_collection_obj(db_obj, collection_name)
    mongo_obj.insert_data_by_collection(collection_obj, nums)

    for i in collection_obj.find():
        print(i)
# mycol =
# dic = {'loc': "Shot_Guard", "id": 10000}
#
# mycol.insert_one(dic)
#
# for i in range(1000):
#     dic_ = {'loc': "Shot_Guard", "id": i}
#     mycol.insert_one(dic_)

# cl_names = db.list_collection_names()
# print(cl_names)
# print(mycol.count())
# print(db.NBA.find())
# dblist = client.list_database_names()

# print(dblist)


if __name__ == '__main__':
    run(ip, port, database_for_test, cl_for_test, 10)

    # cl = MongoClient("mongodb://10.180.116.17:30515")
    # print(cl.list_database_names())
    # db = cl['chris-wang']
    # c = db.list_collection_names()
    # print(c)
