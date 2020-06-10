#!/usr/bin/python
# coding: utf-8
import glob
import re
from lxml import etree



# First step: extraction of the price
def price_extractor(input_list):
    output_dict = {}
    for item in input_list:
        id = item[1]
        desc = item[0]
        last_element = re.split("[\s]", desc)[-1]
        pattern = re.compile("[0-999]")
        dict_values = {}
        if pattern.match(last_element):
            dict_values["price"] = last_element
            output_dict[id] = dict_values
        else:
            output_dict[str(id)] = "none"
    return(output_dict)


def desc_extractor(input):
    """

    :return: a list that contains all of the tei:desc elements
    """
    with open(input, 'r+') as fichier:
        tei = {'tei': 'http://www.tei-c.org/ns/1.0'}
        f = etree.parse(fichier)
        root = f.getroot()
        desc = root.xpath("//tei:desc", namespaces=tei)
        list_desc = []
        for i in desc:
            id = i.xpath("parent::tei:item/@xml:id", namespaces=tei)
            if len(id) > 0:
                i = clean_text(i.text)
                id = id[0]
                list_desc.append([i,id])
        return list_desc



def clean_text(text):
    text = re.sub('	', ' ', text)
    text = re.sub('\n', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub('«$', '', text)
    text = re.sub('»$', '', text)
    text = re.sub('-$', '', text)
    text = re.sub('\s+$', '', text)
    return text


def conversion_to_list(path):
    final_list = []
    for xml_file in glob.iglob(path):
        print(xml_file)
        for desc_element in desc_extractor(xml_file):
            final_list.append(desc_element)
    return final_list


if __name__ == "__main__":
    list_desc = conversion_to_list("../../Data/*.xml")
    output_dict = price_extractor(list_desc)
    print(output_dict)
