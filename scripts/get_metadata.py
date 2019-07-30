#!/usr/local/pythonenvs/decifr-rest/bin/python

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
fh = logging.FileHandler('/var/www/wsgi/decifr-rest/logs/logs.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s, %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%m/%d %H:%M:%S'
)
fh.setFormatter(formatter)
logger.addHandler(fh)

tmp_dir = "/var/www/html/tbas2_1/tmp"


def get_query(runid, query, tmp_dir="/var/www/html/tbas2_1/tmp"):
    retval = {}
    with open("%s/phyloxml_cifr_%s.xml" % (tmp_dir, runid)) as fp:
        tree = etree.parse(fp)
    root = tree.getroot()

    for x in root:
        if x.tag == '{http://www.cifr.ncsu.edu}otus':
            otus = x

    logger.debug(root)
    if not otus:
        raise Exception("no queries found")

    expr = ".//x:name[text() = $name]"
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
    clade = element.getparent()

    for element in clade.iter('{http://www.cifr.ncsu.edu}attribute'):
        name = element[0].text
        value = element[1].text
        retval[name] = value

    all_data = {
        "query": retval
    }
    placement = {}

    otu = element.getparent().getparent().getparent()
    logger.debug(otu.tag)
    for taxon in otu.iter('{http://www.cifr.ncsu.edu}taxon'):
        name = taxon[0].text
        value = taxon[1].text
        placement[name] = value

    all_data["placement"] = placement

    return json.dumps(all_data, indent=4)

    # return json.dumps({"hello": "world"})


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

