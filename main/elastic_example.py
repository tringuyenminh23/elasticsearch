import requests
from elasticsearch import Elasticsearch
import json
from config import root_path
from pprint import pprint

def set_up():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    check_status = requests.get('http://localhost:9200')
    if check_status.status_code != 200:
        raise ('Cannot connect to ElasticSearch server')
    return es


def test_cran():
    es = set_up()
    es.indices.delete(index='cran', ignore=[404])
    with (root_path() / 'data' / 'cran' / 'cran_documents.json').open() as f:
        docs = json.load(f)
    for d in docs:
        es.index(index='cran', doc_type='document', id=d['I'], body=d)

es = set_up()
# res = es.get(index='cran', doc_type='document', id=5)
res = es.search(index="cran", body={"query": {"match": {'W':'what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft .'}}})

for hit in res['hits']['hits']:
    print(hit['_id'])

# pprint(res['hits'])


# print('###')
# res = es.search(index="cran", body={"query":
#                                         {"multi_match": {
#                                             'query': 'what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft .',
#                                             'fields': ['A', 'B', 'W', 'T']}
#                                         }
#                                     })


# pprint(res['hits'])
# test_cran()


#
#
# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }
# res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
# print(res['result'])
#
# res = es.get(index="test-index", doc_type='tweet', id=1)
# print(res['_source'])
#
# es.indices.refresh(index="test-index")
#
# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])