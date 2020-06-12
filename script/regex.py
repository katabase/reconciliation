#!/usr/bin/python
# coding: utf-8
import glob
import re
import json
from lxml import etree



# First step: extraction of the price
def price_extractor(descList):
    """
    TODO: fix the problem of inconsistency between the lenght of the input list and the lenght of the output dict
    :param descList: the list containing all of the tei:desc
    :return: a dict with the ids as keys, and value another dict with the prices
    """
    output_dict = {}
    for item in descList:
        id = item[1]
        desc = item[0]
        raw_price = re.split("[\s]", desc)[-1] # usually the price is the last information of the tei:desc nodes
        pattern_0 = re.compile("^\d{1,3}$") # searches for any non decimal number
        pattern_0b = re.compile("^\d{1,3}\.\d{1,3}$") # searches for any decimal numbers
        # exceptional rules
        pattern_1 = re.compile(".*\.\d$") # searches for this kind of values: "Rare.75"
        pattern_2 = re.compile("in-\d°\d") # searches for this kind of values: "in-4°50"
        pattern_3 = re.compile("^(?!.*in)(-\d*)$") # searches for this kind of values: "-5", ignoring any string that
        # corresponds to a measure (in-4, in-8, etc.)
        dict_values = {"desc": desc}
        if pattern_0.match(raw_price):
            dict_values["price"] = raw_price
        elif pattern_0b.match(raw_price):
            dict_values["price"] = raw_price
        elif pattern_1.match(raw_price):
            price = re.sub(r".*\.(\d)", r"\1", raw_price)
            dict_values["price"] = price
        elif pattern_2.match(raw_price):
            price = re.sub(r"in-\d°(\d)", r"\1", raw_price)
            dict_values["price"] = price
        elif pattern_3.match(raw_price):
            price = re.sub(r"^(?!.*in)-(\d*)$", r"\1", raw_price)
            dict_values["price"] = price
        else:
            dict_values["price"] = "none"
            no_price_trigger()
        output_dict[id] = dict_values
    return(output_dict)


# Second, the extraction of the date
def date_extractor(descList, input_dict):
    """
    TODO: extend the algorithm to the full dates (day and month if possible)
    TODO: find a way to manage the revolutionnary calendar ("30 pluviôse an XIII")
    :param descList: the list containing all of the tei:desc
    :param input_dict: the dictionnary containing the data previously extracted (at this moment, only the price)
    :return: a dict which keys are the ids, and which values are another dict with prices and dates
    """
    for item in descList:
        id = item[1]
        desc = item[0]
        pattern_date_0 = re.compile(".*(1[5-9][0-9][0-9]).*") # we search for any series of four digits
        dict_values = {"desc": input_dict[id].get("desc")}
        if pattern_date_0.match(desc):
            # on va tokéniser avec la virgule comme délimiteur.
            tokenizedDesc = desc.split(",")
            newList = []
            for item in tokenizedDesc:
                if pattern_date_0.match(item):
                    newList.append(item)
            newList = newList[-1]
            newList = newList.split(";")
            for elem in newList:
                if pattern_date_0.match(elem):
                    newList = elem
            newList = re.split("(1[5-9][0-9][0-9])", newList)
            newList = newList[:-1]
            newList = ' '.join([str(elem) for elem in newList])
            newList = newList.split(":")
            for elem in newList:
                if pattern_date_0.match(elem):
                    newList = elem
            newList = re.sub(r'\s+', ' ', newList)
            newList = re.sub(r'\(', '', newList)
            newList = re.sub(r'^\s+', '', newList)
            date = re.sub(r'L\. a\. s\.', '', newList)



            print("%s: %s [%s]" % (id, date, desc))

            dict_values["price"] = input_dict[id].get("price")
            dict_values["date"] = date
            output_dict[id] = dict_values
        else:
            dict_values["price"] = input_dict.get(id).get("price")
            dict_values["date"] = "none"
            output_dict[id] = dict_values
            no_date_trigger()
    return(output_dict)


def no_price_trigger():
    """
    :return: Increases the counter when called
    """
    global no_price
    no_price += 1

def no_date_trigger():
    """
    :return: Increases the counter when called
    """
    global no_date
    no_date += 1

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
            if len(id) > 0: # some of the tei:item do not contain any identifier. We ignore them.
                i = clean_text(i.text)
                id = id[0]
                list_desc.append([i,id])
        return list_desc



def clean_text(input_text):
    """
    A function that cleans the text
    :param text: any string
    :return: the cleaned string
    """
    input_text = re.sub('	', ' ', input_text)
    input_text = re.sub(r'\.$', '', input_text)
    input_text = re.sub(r'-$', '', input_text)
    input_text = re.sub('\n', ' ', input_text)
    input_text = re.sub('\s+', ' ', input_text)
    input_text = re.sub('«$', '', input_text)
    input_text = re.sub('»$', '', input_text)
    output_text = re.sub('\s+$', '', input_text)
    return output_text


def conversion_to_list(path):
    final_list = []
    for xml_file in glob.iglob(path):
        for desc_element in desc_extractor(xml_file):
            final_list.append(desc_element)
    return final_list


if __name__ == "__main__":
    no_price = 0
    no_date = 0
    list_desc = conversion_to_list("../../Data/*.xml")
    print("Total number of tei:desc elements: %s" % len(list_desc))
    output_dict = price_extractor(list_desc)
    print("Lenght of the dictionnary (prices): %s" % len(output_dict.keys()))
    output_dict = date_extractor(list_desc, output_dict)
    print("Lenght of the dictionnary (prices + dates): %s" % len(output_dict))
    with open('../json/export.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(output_dict, outfile)
    print("Number of entries without price: %s" % str(no_price))
    print("Number of entries without date: %s" % str(no_date))
