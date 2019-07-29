#!/usr/local/pythonenvs/decifr-rest/bin/python

import traceback
import sys
# from lxml import etree
from lxml.etree import XMLParser
from lxml.etree import parse
import json


def get_queries(run_id, TMP_FOLDER="/var/www/html/tbas2_1/tmp"):
    xmlfile = "%s/phyloxml_cifr_%s.xml" % (TMP_FOLDER, run_id)
    p = XMLParser(huge_tree=True)
    tree = parse(xmlfile, parser=p)
    root = tree.getroot()
    name_list = []

    for x in root:
        if x.tag == '{http://www.cifr.ncsu.edu}otus':
            otus = x

    for cnt, element in enumerate(
        otus.iter('{http://www.cifr.ncsu.edu}placement')
    ):
        name_list.append(element[0].text)
        if cnt > 5000:
            # break
            pass
    return json.dumps(name_list, indent=4)


def main(run_id, TMP_FOLDER="/var/www/html/tbas2_1/tmp"):
    # raise Exception("dev")
    print(run_id)
    xmlfile = "%s/phyloxml_cifr_%s.xml" % (TMP_FOLDER, run_id)
    p = XMLParser(huge_tree=True)
    tree = parse(xmlfile, parser=p)
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
