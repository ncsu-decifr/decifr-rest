#!/usr/local/pythonenvs/decifr-rest/bin/python

import traceback
import sys
from lxml import etree
from lxml.etree import XMLParser
from lxml.etree import parse
import json


TMP_FOLDER = "/var/www/html/tbas2_1/tmp"


def main(run_id):
    # raise Exception("dev")
    print(run_id)
    xmlfile = "%s/phyloxml_cifr_%s.xml" % (TMP_FOLDER, run_id)
    p = XMLParser(huge_tree=True)
    tree = parse(xmlfile, parser=p)
    print(tree)
    root = tree.getroot()
    name_list = []

    for x in root:
        if x.tag == '{http://www.phyloxml.org}phylogeny':
            phylogeny = x

    for cnt, element in enumerate(
        phylogeny.iter('{http://www.phyloxml.org}name')
    ):
        name_list.append(element.text)
        if cnt > 5000:
            # break
            pass
    return json.dumps(name_list, indent=4)



if __name__ == '__main__':
    try:
        run_id = sys.argv[1]
        retval = main(run_id)
        print(retval)
    except Exception:
        error = traceback.format_exc()
        print(error)