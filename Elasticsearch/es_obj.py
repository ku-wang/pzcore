from elasticsearch import Elasticsearch


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


es = ElasticSearch('10.180.128.11', port=31731)


print(es.ping())
print(es.cluster_health())

print(es.node_info())
print(es.indices())