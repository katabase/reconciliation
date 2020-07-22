#!/usr/bin/python
# coding: utf-8
import shutil
import os
import glob
import re
import json
import dateparser
import datetime
from decimal import *
import rep_greg_conversion
import conversion_tables
from dateparser.search import search_dates
from lxml import etree
import xml.etree.ElementTree as ET
from xml.etree import ElementTree


files = "/home/mgl/Bureau/These/Communications_articles_JE/dh_2020/reconciliation/input/Data_clean/CAT*.xml"
input_dir = os.path.dirname(files)
corpus = "/home/mgl/Bureau/These/Communications_articles_JE/dh_2020/reconciliation/input/Data_clean/corpus.xml"


def conversion_to_list(path):
    final_list = []
    for xml_file in glob.iglob(path):
        final_list.append(xml_file)
    return final_list


def xml_output_production(final_list):
    """
    Creates xi:include links to each of the xml file contained in Data_clean
    :param final_list: a list containing all the paths
    :return:
    """
    print("Updating the xml files")
    tei_namespace = "http://www.tei-c.org/ns/1.0"
    NSMAP1 = {'tei': tei_namespace}  # pour la recherche d'éléments avec la méthode xpath
    ElementTree.register_namespace("", tei_namespace)  # http://effbot.org/zone/element-namespaces.htm#preserving
    # -existing-namespace-attributes
    with open(corpus, 'r+') as fichier:
        f = etree.parse(fichier)
        output_root = f.getroot()
        for path_file in final_list:
            output_root.insert(2, etree.fromstring("<xi:include xmlns:xi=\"http://www.w3.org/2001/XInclude\" href=\"%s\"/>" % path_file))
            corpus_out = "/home/mgl/Bureau/These/Communications_articles_JE/dh_2020/reconciliation/input/Data_clean/corpus_out.xml"

    with open(corpus_out, "w+") as sortie_xml:
        output = etree.tostring(output_root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode(
            'utf8')
        print(output)
        sortie_xml.write(str(output))

final_list = conversion_to_list(files)
xml_output_production(final_list, corpus)