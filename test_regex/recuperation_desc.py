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
            dernier_item = i.text.split(" ")[-1]
            pattern = re.compile("[0-999]")
            if pattern.match(dernier_item):
                trigger_price()
        return desc


def trigger_price():
    global n
    n += 1

def total_number():
    global p
    p += 1

if __name__ == "__main__":
    n = 0
    p = 0
    with open("desc.txt", "w") as output:
        for i in glob.iglob('../../Data/*.xml'):
            for j in desc_extractor(i):
                total_number()
                output.write("%s\n" % j.text.replace('\n', ' '))
    print("Items with price: %s" % n)
    print("Total numbers: %s" % p)