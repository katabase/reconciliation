import glob
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
    return desc


if __name__ == "__main__":
    with open("desc.txt", "w") as output:
        for i in glob.iglob('../../Data/*.xml'):
            for j in desc_extractor(i):
                output.write("%s\n" % j.text)
