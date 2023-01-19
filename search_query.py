from elasticsearch import Elasticsearch

def query_string_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        }
    }
    return q


def multi_match_search(query, fields):
    q = {
        "query": {
            "multi_match": {
                "query":    query,
                "fields": fields
            }
        }
    }
    return q

def search_metaphor(query, fields, metaphor):
    return {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "metaphors.target": {
                            "query": metaphor
                        }
                    }
                },
                "should": {
                    "multi_match": {
                        "query":    query,
                        "fields": fields
                    }
                }
            }
        }
    }

INDEX = 'metaphor-search-engine'
client = Elasticsearch(HOST="http://localhost", PORT=9200,
                       http_auth=('elastic', 'T=e-Dzl7jHLgceEnJFQe'))


def search(query, filter, fields, metaphor):
   
    if (metaphor):
        query_body = search_metaphor(query, fields, metaphor)
    else:
        query_body = multi_match_search(
            query, fields, metaphor) if filter else query_string_search(query)
   
    res = client.search(index=INDEX, body=query_body)
    return res