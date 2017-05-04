 #!/usr/bin/python3
# -*- coding: utf-8 -*-

from io import open
import json
import mock
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

from src import model,utils,toEDX,toIMS

TEST_EDX_DIR = "./testEDX"


def setUp():
    """
    Build EDX folder based on coursTest
    """
    with open("coursTest/module1/module_test.md", encoding='utf-8') as sample_file:
        global m
        m = model.Module(sample_file, "tests", "http://culturenumerique.univ-lille3.fr")
        m.toHTML()
        m_json = json.loads(m.toJson(), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        if os.path.isdir(TEST_EDX_DIR):
            shutil.rmtree(TEST_EDX_DIR)
        m.edx_archive_path = toEDX.generateEDXArchive(m, TEST_EDX_DIR)
        sample_file.close()
        del m_json,sample_file

class EDXArchiveTestCase(unittest.TestCase):


    def testCreationDossierEdx(self):
        """
        Check if all directories and files are created
        """
        self.assertTrue(os.path.isdir(TEST_EDX_DIR),"dir "+TEST_EDX_DIR+" don't exist")
        self.assertTrue(os.path.exists(TEST_EDX_DIR+'/tests_edx.tar.gz'), "tar.gz don't exist")
        self.assertTrue(os.path.isdir(TEST_EDX_DIR+'/EDX'), "dir EDX don't exist")
        self.assertTrue(os.path.exists(TEST_EDX_DIR+'/EDX/course.xml'), "file course.xml don't exist")
        self.assertTrue(os.path.exists(TEST_EDX_DIR+'/EDX/about/overview.html'), "file overview.html don't exist")
        self.assertTrue(os.path.exists(TEST_EDX_DIR+'/EDX/assets/assets.xml'), "file assets.xml don't exist")
        self.assertTrue(os.path.isdir(TEST_EDX_DIR+'/EDX/html'), "dir html don't exist")
        self.assertTrue(os.path.exists(TEST_EDX_DIR+'/EDX/info/updates.html'), "file updates.html don't exist")
        self.assertTrue(os.path.isdir(TEST_EDX_DIR+'/EDX/policies'), "dir policies don't exist")
        self.assertTrue(os.path.isdir(TEST_EDX_DIR+'/EDX/problem'), "dir problem don't exist")

        print("[EDXArchiveTestCase]-- check_creation_dossier_edx OK --")

    def testNbWebContent(self):
        """
        Check the correct number of WebContent's courses
        """
        list_files_html = os.listdir(TEST_EDX_DIR+'/EDX/html')
        self.assertEqual(len(list_files_html), 6, "Not the same numbers of HTML's files")
        print("[EDXArchiveTestCase]-- check_nb_web_content OK --")

    def testNbProblems(self):
        """
        Check the correct number of Activities
        """
        list_files_problems = os.listdir(TEST_EDX_DIR+'/EDX/problem')
        self.assertEqual(len(list_files_problems), 20, "Not the same numbers of Problem's files")

        print("[EDXArchiveTestCase]-- check_nb_problems OK --")

    def testCntCours(self):
        """
        Check the file course.xml
        """
        cpt_act = 0
        cpt_comp = 0
        cpt_act_av = 0
        #transform xml files in XLM object Python
        tree = etree.parse(TEST_EDX_DIR+'/EDX/course.xml')
        #Collect all sequential tag in tree & test existence
        list_seq = tree.xpath("/course/chapter/sequential")
        self.assertNotEquals(list_seq, [])
        for i,vert in enumerate(list_seq):
            # Check if sequential have only one vertical tag
            self.assertEquals(len(vert),1,"Lenght vertical n°"+str(i)+" > 1")
            fm = vert.attrib.get("format")
            if fm == "Activite":
                cpt_act += 1
            elif fm == "Activite Avancee":
                cpt_act_av += 1
            elif fm == "Comprehension":
                cpt_comp += 1
        #Collect all chapter tag in tree
        list_chap = tree.xpath("/course/chapter")
        self.assertNotEquals(list_chap, [])
        #Collect all problem tag in tree
        list_pro = tree.xpath("/course/chapter/sequential/vertical/problem")
        self.assertNotEquals(list_pro, [])
        #Collect all html tag in tree
        list_html = tree.xpath("/course/chapter/sequential/vertical/html")
        self.assertNotEquals(list_html, [])


        #ASSERTS XML TREE
        self.assertEquals(len(list_pro),20,"Not the same nb of problems")
        self.assertEquals(len(list_chap),4,"Not the same nb of chapters")
        self.assertEquals(len(list_seq),15,"Not the same nb of sequentials")
        self.assertEquals(len(list_html),6,"Not the same nb of webcontent")

        #ASSERTS CNT
        self.assertEquals(cpt_act,3,"Not the same nb of Activite")
        self.assertEquals(cpt_act_av,2,"Not the same nb of ActiviteAvancee")
        self.assertEquals(cpt_comp,4,"Not the same nb of Comprehension")

        print("[EDXArchiveTestCase]-- check_nb_cnt_cours OK --")

    def testCNVideo(self):
        """
        Test if video is correctly formating and insert into course.xml
        """
        tree = etree.parse(TEST_EDX_DIR+'/EDX/course.xml')
        root = tree.getroot()
        l_video = root.iter('cnvideo')
        vid = l_video.next()
        self.assertEquals(vid.attrib.get('url_name'),'1-1-1-https-vimeo-com-122104210')
        vid = l_video.next()
        self.assertEquals(vid.attrib.get('url_name'),'1-3-1-https-vimeo-com-122104443')
        vid = l_video.next()
        self.assertEquals(vid.attrib.get('url_name'),'2-3-1-https-vimeo-com-122104499')
        vid = l_video.next()
        self.assertEquals(vid.attrib.get('url_name'),'1-4-1-https-vimeo-com-122104174')

    # def testProblem(self):
    #     class Q

    def runTest(self):
        self.testCreationDossierEdx()
        self.testNbWebContent()
        self.testNbProblems()
        self.testCntCours()
        self.testCNVideo()


# Main
if __name__ == '__main__':
    setUp()
    unittest.main(verbosity=1)
