#!/usr/bin/python
# coding: utf-8
import glob
import re
import json
import dateparser
import datetime
import rep_greg_conversion
from conversion_tables import *
from dateparser.search import search_dates
from lxml import etree
import xml.etree.ElementTree as ET
from xml.etree import ElementTree



# First step: extraction of the price
def price_extractor(descList):
    """
    Extracts the prices of the manuscripts sold and described in the tei:desc.
    TODO: fix the problem of inconsistency between the length of the input list and the length of the output dict
    :param descList: the list containing all of the tei:desc
    :return: a dict with the ids as keys, and value another dict with the prices
    """
    output_dict = {}
    for item in descList:
        id = item[1]
        desc = item[0]
        desc = clean_text(desc)
        raw_price = re.split("[\s]", desc)[-1]  # usually the price is the last information of the tei:desc nodes
        integer_pattern = re.compile("^\d{1,3}$")  # searches for any non decimal number
        decimal_pattern = re.compile("^\d{1,3}\.\d{1,3}$")  # searches for any decimal numbers
        # exceptional rules
        pattern_1 = re.compile(".*\.\d$")  # searches for this kind of values: "Rare.75"
        pattern_2 = re.compile("in-\d°\d")  # searches for this kind of values: "in-4°50"
        pattern_3 = re.compile("^(?!.*in)(-\d*)$")  # searches for this kind of values: "-5", ignoring any string that
        # corresponds to a measure (in-4, in-8, etc.)
        dict_values = {"desc": desc}
        if integer_pattern.match(raw_price):
            position = re.search("\d{1,3}$", desc).span()
            price = raw_price
            start_position = position[0]
            end_position = position[1]
        elif decimal_pattern.match(raw_price):
            position = re.search("\d{1,3}\.\d{1,3}$", desc).span()
            price = raw_price
            start_position = position[0]
            end_position = position[1]
        elif pattern_1.match(raw_price):
            position = re.search(".*\.(\d)$", desc).span(1)
            price = re.sub(r".*\.(\d)", r"\1", raw_price)
            start_position = position[0]
            end_position = position[1]
        elif pattern_2.match(raw_price):
            position = re.search("in-\d°(\d)", desc).span(1)
            price = re.sub(r"in-\d°(\d)", r"\1", raw_price)
            start_position = position[0]
            end_position = position[1]
        elif pattern_3.match(raw_price):
            position = re.search("(?!.*in)-(\d*)", desc).span(1)
            price = re.sub(r"^(?!.*in)-(\d*)$", r"\1", raw_price)
            start_position = position[0]
            end_position = position[1]
        else:
            price = None
            no_price_trigger()
            start_position = None
            end_position = None
        dict_values["price"] = price
        if start_position and end_position:
            desc_xml = "<desc xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022>%s<measure xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 quantity=\u0022%s\u0022 " \
                       "type=\u0022price\u0022>%s</measure>%s</desc>" \
                       % (desc[:start_position], price, desc[start_position:end_position], desc[end_position:])
            if isInt(dict_values["price"]):  # we convert the given price to integers
                dict_values["price"] = int(dict_values["price"])
        else:
            desc_xml = "<desc xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022>%s</desc>" % desc  # to avoid using the variable corresponding to the previous entry
        dict_values["desc_xml"] = desc_xml
        output_dict[id] = dict_values
        item[0] = desc_xml
    return (output_dict)


# Second, the extraction of the date
def date_extractor(descList, input_dict):
    """
    Extracts the dates from the list containing all of the tei:desc, and update the main dict.
    :param descList: the list containing all of the tei:desc
    :param input_dict: the dictionnary containing the data previously extracted (at this moment, only the price)
    :return: a dict which keys are the ids, and which values are another dict with prices and dates
    """
    for item in descList:
        id = item[1]
        desc = item[0]
        desc = clean_text(desc)
        loose_gregorian_calendar_pattern = re.compile(
            ".*(1[0-9][0-9][0-9]).*")  # we search for any series of four digits
        republican_calendar_pattern = re.compile(
            ".*\san ([XIVxiv]{1,4}|[0-9]{1,2}).*")  # we search for any hint of the republican calendar (in
        # general, "an" and a year in roman)
        dict_values = input_dict[id]
        date_path = None
        date_range = None
        desc_xml = desc
        # Let's extract the gregorian calendar dates.
        # Example: "Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798, 1 p. in-8 obl. 22"
        if loose_gregorian_calendar_pattern.match(desc):
            date_path = 1
            # First, we start reducing the string with a first split using the comma as delimiter, as (usually) there
            # is no comma in a date:
            # ['Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798', ' 1 p. in-8 obl. 22']
            tokenizedDesc = desc.split(",")
            string_list = []
            for tok_item in tokenizedDesc:
                if loose_gregorian_calendar_pattern.match(tok_item):
                    string_list.append(tok_item)
            # we can reduce the list to its last element: it will contain the date, as (usually) there is only a
            # single date:
            # ['Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798']
            string_list = string_list[-1]

            # Second, we can reduce the string using the semi colon as delimiter.
            # In our example, it won't affect the string.
            string_list = string_list.split(";")
            for elem in string_list:
                if loose_gregorian_calendar_pattern.match(elem):
                    string_list = elem
            # We split the string by the date, keeping it. The year beeing the delimiter, everything after it is not
            # a date. No change in our example
            string_list = re.split("(1[0-9][0-9][0-9])", string_list)
            string_list = string_list[:-1]
            date_string = ' '.join([str(elem) for elem in string_list])

            # Third, we reduce the string using the colon as delimiter.
            # '18 janvier 1798'
            date_string = date_string.split(":")
            for elem in date_string:
                if loose_gregorian_calendar_pattern.match(elem):
                    date_string = elem
            # Etc.
            date_string = date_string.split("«")
            for elem in date_string:
                if loose_gregorian_calendar_pattern.match(elem):
                    date_string = elem
            date_string = date_string.split(">")
            for elem in date_string:
                if loose_gregorian_calendar_pattern.match(elem):
                    date_string = elem
            # Then we clean the string
            date_string = re.sub(r'\s+', ' ', date_string)
            date_string = re.sub(r'\(', '', date_string)
            date_string = re.sub(r'L\. a\. s\.', '', date_string)
            # And eventually we can extract the date as a string to process it
            date = re.sub(r'^\s', '', date_string)

            gregorian_year_pattern = re.compile("^1[0-9][0-9][0-9]$")  # this pattern matches strings that contains
            # only a year

            # If the date is a year and nothing else, no need to process it.
            if gregorian_year_pattern.match(date):
                date_path = 2
                date_range = re.search("%s" % date, desc).span()
                start_position = date_range[0]
                end_position = date_range[1]
                desc_xml = "%s<date " \
                           "xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 when=\u0022%s\u0022>%s</date>%s" \
                           % (desc[:start_position], date, desc[start_position:end_position],
                              desc[end_position:])
            else:
                date_path = 3
                split_date = date.replace("(", "").replace(")", "").replace("[", "").split(" ")
                date_string = " ".join(split_date)
                parsed_date = dateparser.date.DateDataParser().get_date_data(u'%s' % date)
                if parsed_date["date_obj"] is None:  # if it doesn't work, we select the YYYY string.
                    date_path = 4
                    date = re.search("(1[0-9][0-9][0-9])", date).group(0)
                else:
                    date_range = re.search("(1[0-9][0-9][0-9])", date).span()
                    date_path = 5
                    # We get the precision of the date: dateparser will autocomplete
                    # the date using the current date if it has only the month. That is not what we want.
                    if parsed_date["period"] == "month":
                        date = parsed_date["date_obj"].strftime('%Y-%m')
                    elif parsed_date["period"] == "year":  # this statement should never be true
                        date = parsed_date["date_obj"].strftime('%Y')
                    else:
                        date = parsed_date["date_obj"].strftime('%Y-%m-%d')
                print("split date: %s; id: %s" % (split_date, id))
                if split_date[0] == "": # if we have only a year, the result of the split can be ['', 'YYYY']
                    search = re.search("%s" % split_date[-1], desc)
                elif split_date[0] == ".":
                    search = re.search("%s" % split_date[-1], desc)
                else:
                    print(date_string)
                    search = re.search(date_string, desc)
                print(desc)
                date_range = search.span()
                start_position = date_range[0]
                end_position = date_range[1]
                desc_xml = "%s<date " \
                           "xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 date=\u0022%s\u0022 " \
                           "type=\u0022length\u0022>%s</date>%s" \
                           % (desc[:start_position], date, desc[start_position:end_position],
                              desc[end_position:])
            print(desc_xml)
            dict_values["date_range"] = date_range
            dict_values["date_path"] = date_path
            dict_values["date"] = date

        # If we do not match a gregorian year string (YYYY), but a republican year string ('an V', for instance),
        # we convert the republican date
        elif republican_calendar_pattern.match(desc):
            date_path = 6
            date, start_position, end_position = rep_greg_conversion.main(desc)
            if start_position and end_position:
                desc_xml = "%s<date xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 date=\u0022%s\u0022 " \
                           "type=\u0022length\u0022>%s</date>%s" \
                           % (desc[:start_position], date, desc[start_position:end_position],
                              desc[end_position:])
                dict_values["desc_xml"] = desc_xml
            else:
                desc_xml = input_dict[id].get("desc_xml")
            dict_values["date"] = date
        else:
            dict_values["date"] = None
            no_date_trigger()
            desc_xml = input_dict[id].get("desc_xml")
        dict_values["date_range"] = date_range
        output_dict[id] = dict_values
        item[0] = desc_xml
    return output_dict


def isInt(string):
    try:
        int(string)
        result = isinstance(int(string), int)
    except:
        result = False
    return result


def is_float(string):
    try:
        float(string)
        result = isinstance(float(string), float)
    except:
        result = False
    return result


def is_roman(value):
    try:
        value in roman_to_arabic.keys()
        value = roman_to_arabic[value]
        return value
    except:
        return value


def pn_extractor(descList, input_dict):
    page_number_pattern = re.compile(
        "([IVXivx0-9\/]{1,6})\sp\.?\s?([0-5\/]{0,3})")  # this pattern matches the most frequent case.
    pattern_fraction = re.compile("([0-9\/]{1,6})\s?de\s?p\.?")
    for item in descList:
        id = item[1]
        desc = item[0]
        desc = clean_text(desc)
        desc = re.sub(r"\s+", " ", desc)
        desc = desc.replace("p/", "p")
        dict_values = input_dict[id]
        path = None
        page_number = None
        groups = ""
        if re.search(page_number_pattern, desc):
            position_chaîne = re.search(page_number_pattern, desc).span()
            pn_search = re.search(page_number_pattern, desc)
            groups = pn_search.groups()
            first_group = pn_search.group(1)
            second_group = pn_search.group(2)
            if second_group == "":  # if the second group is empty, there is no fraction
                if first_group != "":
                    if isInt(is_roman(first_group.upper())):
                        page_number = int(is_roman(first_group.upper()))
                        path = 1
                    else:
                        try:
                            page_number = fractions_to_float[first_group]
                            path = 2
                        except:
                            page_number = "key error, please check the transcription: %s" % first_group
                            path = 3
            elif first_group != "" and second_group != "":
                if isInt(first_group):
                    value_1 = int(first_group)
                    path = 4
                else:
                    value_1 = is_roman(first_group.upper())  # the price
                    # can be in roman numbers
                    path = 5
                    if isInt(value_1):
                        path = 6
                        pass
                    else:
                        try:
                            value_1 = fractions_to_float[value_1]
                            path = 7
                        except:
                            value_1 = 501
                            path = 8
                if isInt(second_group):
                    value_2 = int(second_group)
                    path = 9
                else:
                    try:
                        value_2 = fractions_to_float[second_group]
                        path = 10
                    except:
                        value_2 = 404
                        path = 11
                page_number = float(value_1) + float(value_2)
            else:
                page_number = None
                path = 12
        elif re.search(pattern_fraction, desc):
            path = 13
            search = re.search("([0-9\/]{1,6})\s?de\s?p\.?", desc)
            position_chaîne = search.span()
            page_number = fractions_to_float[search.group(1)]

        if page_number != None:
            starting_position = position_chaîne[0]
            ending_position = position_chaîne[1]
            if desc[
                ending_position - 1] == " ":  # if a space is the last character of the identified range of page ("1 p. "), we can
                ending_position = ending_position - 1
            desc_xml = "%s<measure xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 quantity=\u0022%s\u0022 " \
                       "type=\u0022length\u0022>%s</measure>%s" \
                       % (desc[:starting_position], page_number, desc[starting_position:ending_position],
                          desc[ending_position:])
        else:
            desc_xml = input_dict[id].get("desc_xml")
        # dict_values["groups"] = groups # for debugging purposes only
        dict_values["path"] = path #idem
        dict_values["desc_xml"] = desc_xml
        dict_values["number_of_pages"] = page_number
        output_dict[id] = dict_values
        item[0] = desc_xml
    return input_dict


def format_extractor(descList, input_dict):
    for item in descList:
        id = item[1]
        desc = item[0]
        dict_values["format"] = ms_format
        dict_values["number_of_pages"] = input_dict.get(id).get("number_of_pages")
        dict_values["date"] = input_dict.get(id).get("date")
        dict_values["price"] = input_dict.get(id).get("price")
        output_dict[id] = dict_values
    return input_dict


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
            if len(id) > 0:  # some of the tei:item do not contain any identifier. We ignore them.
                id = id[0]
                list_desc.append([i.text, id])
        return list_desc


def clean_text(input_text):
    """
    A function that cleans the text
    :param text: any string
    :return: the cleaned string
    """
    input_text = re.sub('\n', ' ', input_text)
    input_text = re.sub('\s+', ' ', input_text)
    output_text = re.sub('\s+$', '', input_text)
    return output_text


def conversion_to_list(path):
    final_list = []
    for xml_file in glob.iglob(path):
        for desc_element in desc_extractor(xml_file)[:10]:  # we select only the 10 first entries to speed up
            # processing (to be deleted)
            final_list.append(desc_element)
    return final_list



def xml_output_production(dict):
    with open("output.xml", 'w') as fichier:
        tei_namespace = "http://www.tei-c.org/ns/1.0"
        tei = "{%s}" % tei_namespace
        NSMAP0 = {None: tei_namespace}  # the default namespace (no prefix)
        NSMAP1 = {'tei': tei_namespace}  # pour la recherche d'éléments avec la méthode xpath
        root = etree.Element(tei + "root", nsmap=NSMAP0)  # https://lxml.de/tutorial.html#namespaces
        root = ElementTree.Element("root")
        #  https://stackoverflow.com/questions/7703018/how-to-write-namespaced-element-attributes-with-lxml
        for key in dict:
            d = dict[key]["desc_xml"]
            print(d)
            c = ElementTree.XML(d)
            root.append(c)
        ElementTree.dump(root)



if __name__ == "__main__":
    no_price = 0
    no_date = 0
    list_desc = conversion_to_list("../../Data/*.xml")
    output_dict = price_extractor(list_desc)
    output_dict = date_extractor(list_desc, output_dict)
    output_dict = pn_extractor(list_desc, output_dict)
    # output_dict = format_extractor(list_desc, output_dict)
    # xml_output_production(output_dict)

    with open('../json/export.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(output_dict, outfile)
    print("Number of entries without price: %s" % str(no_price))
    print("Number of entries without date: %s" % str(no_date))
