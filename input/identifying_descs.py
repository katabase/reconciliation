from lxml import etree
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import glob
import tqdm

def adding_id(file):
    tei_namespace = "http://www.tei-c.org/ns/1.0"
    NSMAP1 = {'tei': tei_namespace}  # pour la recherche d'éléments avec la méthode xpath
    ElementTree.register_namespace("", tei_namespace)  # http://effbot.org/zone/element-namespaces.htm#preserving
    # -existing-namespace-attributes
    with open(file, 'r+') as fichier:
        f = etree.parse(fichier)
        output_root = f.getroot()
        descs = "//tei:item[@xml:id]/tei:desc"
        desc_list = output_root.xpath(descs, namespaces=NSMAP1)
        for desc in desc_list:  # now let's update the tei:desc elements in the output file
            id = desc.xpath("parent::tei:item/@xml:id", namespaces=NSMAP1)
            desc_number = int(desc.xpath("count(preceding::tei:desc) - count(parent::tei:item/preceding::tei:desc) + 1", namespaces=NSMAP1))
            existing_id = output_root.xpath("//*[@xml:id='%s_%s']" % (id[0], desc_number), namespaces=NSMAP1)
            if len(existing_id) == 0:
                desc.set("{http://www.w3.org/XML/1998/namespace}id", "%s_%s" % (id[0], desc_number))
            else:
                print(existing_id)

        output_file = "Data_clean_with_id/%s" % file.split("/")[-1]
        with open(output_file, "w+") as sortie_xml:
            output = etree.tostring(output_root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode(
                'utf8')
            sortie_xml.write(str(output))



if __name__ == "__main__":
    print("Adding xml:id to each tei:desc")
    path = "Data_clean/*.xml"
    for xml_file in glob.iglob(path):
        adding_id(xml_file)
