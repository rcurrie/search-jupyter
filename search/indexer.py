#!/usr/bin/env python3
import os
import sys
import time
import logging
import argparse
from elasticsearch import Elasticsearch


def index_ipynb(es, path):
    """
    Index a jupyter notebook

    See https://github.com/jupyter/nbviewer/blob/master/nbviewer/index.py
    """
    with open(path) as f:
        body = f.read()
    es.index(index="jupyter", doc_type="notebook", id=path, body=body)


def main():
    """
    Jupyter Notebook Indexer

    Builds an elastic search index of jupyter notebooks
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-d", "--debug", action='store_true', default=False,
                        help="Debug output")
    parser.add_argument("-i", "--interval", type=int, default=0,
                        help="Minutes between indexing, default index once and exits")
    parser.add_argument("path", nargs='?', default="",
                        help="Path to start indexing")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    while True:
        start = time.time()
        logging.info("Starting indexing at {}".format(time.asctime(time.localtime(start))))

        try:
            es = Elasticsearch(hosts=["es"])

            for root, dirs, files in os.walk(args.path, topdown=True):
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.' and '.ipynb_checkpoints' not in d]
                for name in files:
                    path = "{}/{}".format(root, name)
                    logging.debug(path)

                    if name.endswith(".ipynb"):
                        index_ipynb(es, path)

            end = time.time()
            logging.info("Finished indexing at {} taking {} seconds".format(
                time.asctime(time.localtime(end)), end - start))
        except Exception as e:
            logging.error("Problems indexing: {}".format(e))

        if args.interval:
            logging.info("Sleeping for {} minutes...".format(args.interval))
            time.sleep(args.interval * 60)
        else:
            break


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()
