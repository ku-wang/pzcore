from elasticsearch import Elasticsearch

index_body = {
            "mappings": {
                "type_doc_test": {                           #type_doc_test为doc_type
                    "properties": {
                        "id": {
                            "type": "long",
                            "index": "false"
                        },
                        "serial": {
                            "type": "keyword",  # keyword不会进行分词,text会分词
                            "index": "false"  # 不建索引
                        },
                        "tags": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "keyword", "index": True},
                                "dominant_color_name": {"type": "keyword", "index": True},
                                "skill": {"type": "keyword", "index": True},
                            }
                        },
                        "hasTag": {
                            "type": "long",
                            "index": True
                        },
                        "status": {
                            "type": "long",
                            "index": True
                        },
                        "createTime": {
                            "type": "date",
                            "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                        },
                        "updateTime": {
                            "type": "date",
                            "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                        }
                    }
                }
            }
        }

doc_body = {
    "id"
}


class ElasticSearch(object):
    _session = None

    def __init__(self, host, port, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @property
    def session(self):
        if self._session is None:
            self._session = Elasticsearch(hosts=self.host, port=self.port)

        return self._session

    def ping(self):
        return self.session.ping()

    def cluster_health(self):

        health_results = self.session.cat.health()
        return health_results

    def node_info(self):
        return self.session.cat.nodes()

    def indices(self):
        return self.session.cat.indices()


es = ElasticSearch('10.180.116.11', port=31157)


print(es.ping())
print(es.cluster_health())

print(es.node_info())
print(es.indices())