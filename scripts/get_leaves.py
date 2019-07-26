#!/usr/local/pythonenvs/decifr-rest/bin/python

import traceback

def main():
    raise Exception("dev")



if __name__ == '__main__':
    try:
        main()
    except Exception:
        error = traceback.format_exc()
        print(error)