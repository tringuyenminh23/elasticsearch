from config import root_path
import json


def parse_cran_file(path):
    def parse_article(article):
        if not article:
            return
        components = article.split('\n.')
        components[0] = ('I', components[0])
        for idx, c in enumerate(components[1:]):
            components[idx + 1] = (c[0], c[2:].replace('\n', ' '))
        return dict(components)
    with path.open() as f:
        articles = [parse_article(art) for art in f.read().split('.I ')]
    return articles[1:]


def cran_to_json():
    documents = parse_cran_file(root_path() / 'data' / 'cran' / 'cran.all.1400')
    with (root_path() / 'data' / 'cran' / 'cran_documents.json').open(mode='w') as f:
        json.dump(documents, f)
    queries = parse_cran_file(root_path() / 'data' / 'cran' / 'cran.qry')
    with (root_path() / 'data' / 'cran' / 'cran_queries.json').open(mode='w') as f:
        json.dump(queries, f)

cran_to_json()
