import requests
import hug


@hug.get("/search", examples="query=leukemia%20relapse%20JAK2")
def search_submissions(query: hug.types.text):
    """ Search submissions for query """
    print("query", query)
    r = requests.post("http://es:9200/jupyter/notebook/_search",
                      json={"query": {"match": {"_all": {"query": query, "operator": "and"}}},
                            "size": 100, "stored_fields": ["id"]})
    return r.json()
