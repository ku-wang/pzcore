from pymongo import MongoClient
import mongo.mongo_data_tmp as mongo_data
import random
import datetime
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED, wait
import copy

# template of data -> for test
ip = '10.180.116.17'
port = 3119
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

    def handle_docs(self, doc_nums):

        def split_list(lists, seg_length):
            inlist = lists[:]
            outlist = []

            while inlist:
                outlist.append(inlist[0:seg_length])
                inlist[0:seg_length] = []
            return outlist

        templates = []
        for num in range(1, doc_nums + 1):
            templates.append(mongo_data.generate_doc())

        return split_list(templates, 1000)

    def insert_doc(self, collection_obj, docs):

        print("Start insert {num} documents to [{connection_name}] ...".
              format(num=len(docs), connection_name=collection_obj.full_name))

        inserted_ids = collection_obj.insert_many(docs)
        print(inserted_ids)

        if len(inserted_ids.inserted_ids) == len(docs):
            print("Insert {num} documents to [{connection_name}] done ...".
                  format(num=len(docs), connection_name=collection_obj.full_name))
        else:
            raise Exception("Insert failed ...")

    def insert_docs_by_collection(self, collection_obj, doc_nums):
        templates = self.handle_docs(doc_nums)

        insert_client_pool = ThreadPoolExecutor(max_workers=20)
        insert_client_futures = [insert_client_pool.submit(self.insert_doc, collection_obj, template) for
                                 template in templates]
        wait(insert_client_futures, return_when=ALL_COMPLETED)

        return True


def run(ip, port, db_name, collection_name, nums=10):
    mongo_obj = Mongo(ip, port)

    db_obj = mongo_obj.get_db_obj(db_name)
    collection_obj = mongo_obj.get_collection_obj(db_obj, collection_name)
    mongo_obj.insert_docs_by_collection(collection_obj, nums)
    for i in collection_obj.find():
        print(i)


def run_multi_collections(ip, port, db_name, collection_name, file_nums=10, collctions=10):
    mongo_obj = Mongo(ip, port)
    db_obj = mongo_obj.get_db_obj(db_name)

    start_time = datetime.datetime.now()

    client_pool = ThreadPoolExecutor(max_workers=20)
    client_futures = [client_pool.submit(mongo_obj.insert_docs_by_collection,
                    mongo_obj.get_collection_obj(db_obj, collection_name+str(collection)), file_nums)
                      for collection in range(collctions)]
    wait(client_futures, return_when=ALL_COMPLETED)

    print("Finish insert ...")

    end_time = datetime.datetime.now()
    take_time = end_time - start_time
    print('Insert take time: {time}'.format(time=take_time))


def check_collections():
    cl = MongoClient("mongodb://10.180.116.17:30515")
    db = cl['chris_wang']
    c = db.list_collection_names()
    print(len(c))
    coll = random.choice(c)

    print(len(list(db[coll].find())))


if __name__ == '__main__':

    run_multi_collections(ip, port, database_for_test, cl_for_test, file_nums=10, collctions=1)
    #
    # check_collections()


