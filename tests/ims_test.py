from io import open
import json
import mock
from pygiftparser import parser as pygift

from lxml import etree
import shutil
from bs4 import BeautifulSoup
import unittest
from collections import namedtuple
from six.moves import StringIO
from jinja2 import Template, Environment, FileSystemLoader
# Path hack for getting access to src python modules
import sys, os
sys.path.insert(0, os.path.abspath('..'))

# Ignore Warning
import logging
logger = logging.getLogger()
logger.setLevel(40)

from src import model, toIMS

TEST_IMS_DIR = "./IMS"

def setUp():
    """
    Build IMS folder based on coursTest
    """
    with open("coursTest/module1/module_test.md", encoding='utf-8') as sample_file:
        global m
        m = model.Module(sample_file, "tests", "http://culturenumerique.univ-lille3.fr")
        m.toHTML()
        m_json = json.loads(m.toJson(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        if os.path.isdir(TEST_IMS_DIR):
            shutil.rmtree(TEST_IMS_DIR)
        m.ims_archive_path = toIMS.generateImsArchive(m, "Truc", "./")
        sample_file.close()
        del m_json,sample_file


# Main
if __name__ == '__main__':
    setUp()
    unittest.main(verbosity=1)
