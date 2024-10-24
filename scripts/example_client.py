"""
Example client script.
"""

import requests
import sys
import os
import json

SERVER = 'https://rest.cifr.ncsu.edu'
USERNAME = 'admin'
PASSWORD = 'password'
LOCAL_DIRECTORY = '/tmp/'

def leaves(run_id):
    print("getting leaves for %s" % run_id)
    work_dir = "%s/decifr-rest%s" % (LOCAL_DIRECTORY, run_id)
    os.makedirs(work_dir, exist_ok = True)
    os.chdir(work_dir)

    leaves_url = "%s/leaves/%s?return_type=json" % (SERVER, run_id)
    r = requests.get(leaves_url, auth=(USERNAME, PASSWORD))
    print(r.status_code)
    if r.status_code != 200:
        print("invalid runid or server error")
        sys.exit()

    with open("leaves.json", "w") as fp:
        fp.write(r.text)

    os.makedirs("leaves", exist_ok = True)
    leaves_json = r.text
    leaves = json.loads(leaves_json)

    for leaf in leaves:
        leaf_url = "%s/leaf/%s/metadata?query=%s&return_type=json" % (
            SERVER, run_id, leaf
        )
        r = requests.get(leaf_url, auth=(USERNAME, PASSWORD))
        if r.status_code != 200:
            continue
        else:
            print(leaf)
            with open("leaves/%s.json" % leaf, "w") as fp:
                fp.write(r.text)

def queries(run_id):
    print("getting queries for %s" % run_id)
    work_dir = "%s/decifr-rest%s" % (LOCAL_DIRECTORY, run_id)
    os.makedirs(work_dir, exist_ok = True)
    os.chdir(work_dir)

    queries_url = "%s/queries/%s?return_type=json" % (SERVER, run_id)
    r = requests.get(queries_url, auth=(USERNAME, PASSWORD))
    print(r.status_code)
    if r.status_code != 200:
        print("invalid runid or server error")
        sys.exit()

    with open("queries.json", "w") as fp:
        fp.write(r.text)

    os.makedirs("queries", exist_ok = True)
    queries_json = r.text
    queries = json.loads(queries_json)

    for query in queries:
        query_url = "%s/query/%s/metadata?query=%s&return_type=json" % (
            SERVER, run_id, query
        )
        r = requests.get(query_url, auth=(USERNAME, PASSWORD))
        if r.status_code != 200:
            continue
        else:
            print(query)
            with open("queries/%s.json" % query, "w") as fp:
                fp.write(r.text)


if __name__ == '__main__':
    try:
        run_id = sys.argv[1]
        mode = sys.argv[2]
    except IndexError:
        print("usage: python example_client.py <run_id> <leaves|queries>")
        sys.exit()

    if mode == 'leaves':
        leaves(run_id)
    if mode == 'queries':
        queries(run_id)