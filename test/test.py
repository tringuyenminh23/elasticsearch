import json
import timeit

import requests
from elasticsearch import Elasticsearch

from config import root_path


def set_up():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    check_status = requests.get('http://localhost:9200')
    if check_status.status_code != 200:
        raise ('Cannot connect to ElasticSearch server')
    return es


def test_cran():
    es = set_up()
    es_version = es.info()['version']['number']

    file_name = es_version + '_cran.txt'

    with (root_path() / 'test' / 'out' / file_name).open(mode='w') as outf:
        outf.write('query_index result_index score')
        # outf.write('elastic search version %s \n' % es_version)
        es.indices.delete(index='cran', ignore=[404])
        with (root_path() / 'data' / 'cran' / 'cran_documents.json').open() as f:
            docs = json.load(f)
        start_indexing = timeit.default_timer()
        for d in docs:
            es.index(index='cran', doc_type='document', id=d['I'], body=d)
        # outf.write('indexing took %.4f\n' %(timeit.default_timer() - start_indexing))

        with (root_path() / 'data' / 'cran' / 'cran_queries.json').open() as f:
            queries = json.load(f)

        for q in queries:
            q_index = int(q['I'])
            elastic_query = {"query": {"match": {"W": q['W']}}}
            res = es.search(index='cran', body=elastic_query)
            for hit in res['hits']['hits']:
                outf.write('%d %s %s\n' %(q_index, hit['_id'], hit['_score']))


test_cran()
