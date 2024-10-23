"""
Example client script.
"""

import requests
import sys
import os

SERVER = 'https://rest.cifr.ncsu.edu/'
USERNAME = 'admin'
PASSWORD = 'secret'
LOCAL_DIRECTORY = '/tmp/'

def main(run_id):
    print("getting data for %s" % run_id)
    work_dir = "%s/decifr-rest%s" % (LOCAL_DIRECTORY, run_id)
    os.makedirs(work_dir, exist_ok = True)
    os.chdir(work_dir)

    leaves_url = "%s/leaves/%s?return_type=json" % (SERVER, run_id)
    r = requests.get(leaves_url, auth=(USERNAME, PASSWORD))

    with open("leaves.json", "w") as fp:
        fp.write(r.text)




if __name__ == '__main__':
    try:
        run_id = sys.argv[1]
    except IndexError:
        print("usage: python example_client.py <run_id>")
    main(run_id)