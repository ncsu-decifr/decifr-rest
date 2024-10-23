"""
#!/usr/local/pythonenvs/decifr-rest/bin/python
"""

import requests
import sys

SERVER = 'https://rest.cifr.ncsu.edu/'
USERNAME = 'admin'
PASSWORD = 'secret'

def main():
    pass

if __name__ == '__main__':
    try:
        run_id = sys.argv[1]
    except IndexError:
        print("usage: python example_client.py <run_id>")
    main()