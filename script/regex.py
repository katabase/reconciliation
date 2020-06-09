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
        if pattern.match(last_element):
            output_dict[str(id)] = last_element
        else:
            output_dict[str(id)] = "none"
    print(output_dict)


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
            i = remove_multiple_spaces(i.text)
            list_desc.append([i,id])
        return list_desc



def remove_multiple_spaces(text):
    text = re.sub('	', ' ', text)
    text = re.sub('\n', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub('\s+$', '', text) # we remove any space ending a line
    return text


def conversion_to_list(path):
    final_list = []
    for xml_file in glob.iglob(path):
        for desc_element in desc_extractor(xml_file):
            final_list.append(desc_element)
    return final_list


if __name__ == "__main__":
    list_desc = conversion_to_list("../../Data/*.xml")
    price_extractor(list_desc)