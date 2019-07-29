#!/usr/local/pythonenvs/dobenv/bin/python

# import datetime
import logging
import os
import json
import sys
import traceback
from lxml import etree


# # pip install pycrypto
# from Crypto.Hash import MD5

logger = logging.getLogger("rest query")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('/var/www/wsgi/decifr/logs/logs.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s, %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%m/%d %H:%M:%S'
)
fh.setFormatter(formatter)
logger.addHandler(fh)

tmp_dir = "/var/www/html/tbas2_1/tmp"


def placement_fn(runid, query):
    retval = {}

    with open("%s/phyloxml_cifr_%s.xml" % (tmp_dir, runid)) as fp:
        tree = etree.parse(fp)
    root = tree.getroot()
    for x in root:
        logger.debug(x)
        if x.tag == '{http://www.cifr.ncsu.edu}otus':
            otus = x

    expr = "//b:placement/x:name[text() = $name]"
    test = otus.xpath(
        expr,
        name=query,
        namespaces={
            'x': 'http://www.phyloxml.org',
            'b': 'http://www.cifr.ncsu.edu'
        }
    )
    if len(test) == 0:
        raise Exception("no species matches query")
    logger.debug(test[0].tag)
    logger.debug(test[0].text)

    element = test[0]

    retval['name'] = query
    retval['placement'] = {}
    retval['attributes'] = {}
    clade = element.getparent().getparent()

    for element in clade.iter('{http://www.cifr.ncsu.edu}taxon'):
        name = element[0].text
        value = element[1].text
        retval['placement'][name] = value

    clade = element.getnext()

    for element in clade.iter('{http://www.cifr.ncsu.edu}attribute'):
        name = element[0].text
        value = element[1].text
        retval['attributes'][name] = value

    return json.dumps(retval, indent=4)


def main(runid, query, tmp_dir="/var/www/html/tbas2_1/tmp"):
    # raise Exception("goodby cruel world")
    retval = {}

    with open("%s/phyloxml_cifr_%s.xml" % (tmp_dir, runid)) as fp:
        tree = etree.parse(fp)
    root = tree.getroot()
    for x in root:
        logger.debug(x)
        if x.tag == '{http://www.phyloxml.org}phylogeny':
            phylogeny = x

    # for element in phylogeny.iter('{http://www.phyloxml.org}name'):
    #     if element.text == query:
    #         retval['name'] = query
    #         clade = element.getparent()
    #     else:
    #         continue
    # e = phylogeny.xpath('.//a[text()="TEXT A"]')
    # expr = "//*[local-name() = $name]"

    expr = ".//x:name[text() = $name]"
    test = phylogeny.xpath(
        expr,
        name=query,
        namespaces={
            'x': 'http://www.phyloxml.org',
            'b': 'http://www.cifr.ncsu.edu'
        }
    )
    if len(test) == 0:
        raise Exception("no species matches query")
    logger.debug(test[0].tag)
    logger.debug(test[0].text)
    element = test[0]

    retval['name'] = query
    clade = element.getparent()

    for element in clade.iter('{http://www.cifr.ncsu.edu}attribute'):
        name = element[0].text
        value = element[1].text
        retval[name] = value

    return json.dumps(retval, indent=4)


if __name__ == '__main__':
    logger.debug(sys.argv)
    runid = sys.argv[1]
    query = sys.argv[2]
    placement = sys.argv[3]
    if query == 'na' and placement != 'na':
        try:
            results = placement_fn(runid, placement)

        except Exception:
            error = traceback.format_exc()
            logger.debug(error)

            results = error

    elif query != 'na' and placement == 'na':
        try:
            results = main(runid, query)

        except Exception:
            error = traceback.format_exc()
            logger.debug(error)

            results = error
    else:
        print "invalid parameters to rest"

    print results
