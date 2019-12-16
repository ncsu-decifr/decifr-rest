"""
#!/usr/local/pythonenvs/decifr-rest/bin/python
"""

# import datetime
import logging
import os
import json
import sys
import traceback
from lxml import etree
from lxml.etree import XMLParser


# # pip install pycrypto
# from Crypto.Hash import MD5

logger = logging.getLogger("rest query")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs/logs.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s, %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%m/%d %H:%M:%S'
)
fh.setFormatter(formatter)
logger.addHandler(fh)

tmp_dir = "/var/www/html/tbas2_1/tmp"


def otu_query(runid, query, tmp_dir="/var/www/html/tbas2_1/tmp"):
    retval = {}
    p = XMLParser(huge_tree=True)
    with open("%s/%s.mep" % (tmp_dir, runid)) as fp:
        tree = etree.parse(fp, parser=p)
    root = tree.getroot()

    for x in root:
        if x.tag == '{http://www.cifr.ncsu.edu}otus':
            otus = x

    logger.debug(root)
    if otus is None:
        raise Exception("no otus found")

    expr = ".//b:name[text() = $name]"
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
    otu = element.getparent()

    retval['otu'] = query
    retval['leaf_name'] = otu[1].text
    retval['taxonomy'] = {}
    retval['otu_strains'] = []

    for element in otu.iter('{http://www.cifr.ncsu.edu}taxon'):
        name = element[0].text
        value = element[1].text
        retval['taxonomy'][name] = value

    for element in otu.iter('{http://www.cifr.ncsu.edu}placement'):
        name = element[0].text
        retval['otu_strains'].append(name)

    return json.dumps(retval, indent=4)


def get_query(runid, query, tmp_dir="/var/www/html/tbas2_1/tmp"):
    retval = {}
    p = XMLParser(huge_tree=True)
    with open("%s/%s.mep" % (tmp_dir, runid)) as fp:
        tree = etree.parse(fp, parser=p)
    root = tree.getroot()

    for x in root:
        if x.tag == '{http://www.cifr.ncsu.edu}otus':
            otus = x

    if otus is None:
        raise Exception("no queries found")

    expr = ".//x:name[text() = $name]"
    test = otus.xpath(
        expr,
        name=query,
        namespaces={
            'x': 'http://www.cifr.ncsu.edu',
            'b': 'http://www.cifr.ncsu.edu'
        }
    )
    if len(test) == 0:
        raise Exception("no species matches query")
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
    sequences = {}
    for element in clade.getparent().iter('{http://www.cifr.ncsu.edu}sequence'):
        name = element[0].text
        value = element[1].text
        sequences[name] = value
    all_data["sequences"] = sequences
    placement = {}

    otu = element.getparent().getparent().getparent()
    for taxon in otu.iter('{http://www.cifr.ncsu.edu}taxon'):
        name = taxon[0].text
        value = taxon[1].text
        placement[name] = value

    all_data["placement"] = placement
    return json.dumps(all_data, indent=4)


def main(runid, query, tmp_dir="/var/www/html/tbas2_1/tmp"):
    # raise Exception("goodby cruel world")
    retval = {}
    p = XMLParser(huge_tree=True)

    with open("%s/%s.mep" % (tmp_dir, runid)) as fp:
        tree = etree.parse(fp, parser=p)
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

