from pymongo import MongoClient
import mongo.mongo_data_tmp as mongo_data
import random
import datetime
import copy
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait

# template of data -> for test
data_template = {"loc": '', "name": '', "date": '', "company": "EVI", "department": "QA", "Group": "CORE",
                 "Tester": "HandSomeChris"}
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

    def get_db_obj(self, db_name):
        return self._client[db_name]

    def get_collection_obj(self, db_obj, connection_name):
        return db_obj[connection_name]

    def list_all_collections(self, db_obj):
        return db_obj.list_collection_names()

    def insert_data_by_collection(self, collection_obj, nums):
        templates = []
        for num in range(1, nums+1):
            template = copy.deepcopy(data_template)
            template['loc'] = random.choice(locs)
            template['name'] = mongo_data.generate_random_string(6)
            template['date'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            templates.append(template)

        print("Start insert files to [{connection_name}]".
                  format(num=nums, connection_name=collection_obj.full_name))
        inserted_ids = collection_obj.insert_many(templates)
        if len(inserted_ids.inserted_ids) == nums:
            print("Insert {num} files to [{connection_name}] done ...".
                  format(num=nums, connection_name=collection_obj.full_name))
        else:
            raise Exception("Insert failed ...")
        return True


def run(ip, port, db_name, collection_name, nums=10):
    mongo_obj = Mongo(ip, port)

    db_obj = mongo_obj.get_db_obj(db_name)
    collection_obj = mongo_obj.get_collection_obj(db_obj, collection_name)
    mongo_obj.insert_data_by_collection(collection_obj, nums)
    for i in collection_obj.find():
        print(i)


def run_multi_collctions(ip, port, db_name, collection_name, file_nums=10, collctions=10):
    mongo_obj = Mongo(ip, port)

    db_obj = mongo_obj.get_db_obj(db_name)

    # for collection in range(collctions):
    #     collection_obj = mongo_obj.get_collection_obj(db_obj, collection_name+str(collection))
    #     mongo_obj.insert_data_by_collection(collection_obj, file_nums)

    client_pool = ThreadPoolExecutor(max_workers=10)
    client_futures = [client_pool.submit(mongo_obj.insert_data_by_collection,
                    mongo_obj.get_collection_obj(db_obj, collection_name+str(collection)), file_nums)
                      for collection in range(collctions)]
    wait(client_futures, return_when=ALL_COMPLETED)


def check_collections():
    cl = MongoClient("mongodb://10.180.116.17:30515")
    db = cl['chris_wang']
    c = db.list_collection_names()
    print(len(c))
    coll = random.choice(c)

    print(len(list(db[coll].find())))


if __name__ == '__main__':
    # run(ip, port, database_for_test, cl_for_test, 1000)
    run_multi_collctions(ip, port, database_for_test, cl_for_test, file_nums=1000, collctions=10)

    # check_collections()
