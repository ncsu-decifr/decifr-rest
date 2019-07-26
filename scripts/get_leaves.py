#!/usr/local/pythonenvs/decifr-rest/bin/python

import traceback
import sys
from lxml import etree
from lxml.etree import XMLParser
from lxml.etree import parse


TMP_FOLDER = "/var/www/html/tbas2_1/tmp"


def main(run_id):
    # raise Exception("dev")
    print(run_id)
    xmlfile = "%s/phyloxml_cifr_%s.xml" % (TMP_FOLDER, run_id)
    p = XMLParser(huge_tree=True)
    tree = parse(xmlfile, parser=p)
    print(tree)



if __name__ == '__main__':
    try:
        run_id = sys.argv[1]
        main(run_id)
    except Exception:
        error = traceback.format_exc()
        print(error)