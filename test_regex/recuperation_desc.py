#!/usr/bin/python
# coding: utf-8
import glob
import re
from lxml import etree


def desc_extractor(input):
    """

    :return: a list that contains all of the tei:desc elements
    """
    with open(input, 'r+') as fichier:
        tei = {'tei': 'http://www.tei-c.org/ns/1.0'}
        f = etree.parse(fichier)
        root = f.getroot()
        desc = root.xpath("//tei:desc", namespaces=tei)
        for i in desc:
            i = clean_text(i.text)
            dernier_item = re.split("[\s]", i)[-1]
            pattern = re.compile("[0-999]")
            if pattern.match(dernier_item):
                trigger_price()
            else:
                with open("errs.txt", "a") as err_log:
                    err_log.write("%s (%s)\n" % (dernier_item,i))
        return desc


def clean_text(input_text):
    """
    A function that cleans the text
    :param text: any string
    :return: the cleaned string
    """
    input_text = re.sub('	', ' ', input_text)
    input_text = re.sub(r'-$', '', input_text)
    input_text = re.sub('\n', ' ', input_text)
    input_text = re.sub('\s+', ' ', input_text)
    input_text = re.sub('«$', '', input_text)
    input_text = re.sub('»$', '', input_text)
    output_text = re.sub('\s+$', '', input_text)
    return output_text


def trigger_price():
    global n
    n += 1


def total_number():
    global p
    p += 1


if __name__ == "__main__":
    n = 0
    p = 0
    file = open("errs.txt", "r+")
    file.truncate(0)
    file.close()
    with open("desc.txt", "w") as output:
        for i in glob.iglob('../../Data/*.xml'):
            for j in desc_extractor(i):
                total_number()
                output.write("%s\n" % j.text.replace("\n", " "))
    print("Items with price: %s" % n)
    print("Total numbers: %s" % p)
