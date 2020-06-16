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




# First step: extraction of the price
def price_extractor(descList):
    """
    Extracts the prices of the manuscripts sold and described in the tei:desc.
    TODO: fix the problem of inconsistency between the lenght of the input list and the lenght of the output dict
    :param descList: the list containing all of the tei:desc
    :return: a dict with the ids as keys, and value another dict with the prices
    """
    output_dict = {}
    for item in descList:
        id = item[1]
        desc = item[0]
        raw_price = re.split("[\s]", desc)[-1]  # usually the price is the last information of the tei:desc nodes
        pattern_0 = re.compile("^\d{1,3}$")  # searches for any non decimal number
        pattern_0b = re.compile("^\d{1,3}\.\d{1,3}$")  # searches for any decimal numbers
        # exceptional rules
        pattern_1 = re.compile(".*\.\d$")  # searches for this kind of values: "Rare.75"
        pattern_2 = re.compile("in-\d°\d")  # searches for this kind of values: "in-4°50"
        pattern_3 = re.compile("^(?!.*in)(-\d*)$")  # searches for this kind of values: "-5", ignoring any string that
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
        loose_gregorian_calendar_pattern = re.compile(
            ".*(1[0-9][0-9][0-9]).*")  # we search for any series of four digits
        republican_calendar_pattern = re.compile(
            ".*\san ([XIVxiv]{1,4}|[0-9]{1,2}).*")  # we search for any hint of the republican calendar (in
        # general, "an" and a year in roman)
        dict_values = {"desc": input_dict[id].get("desc")}

        # Let's extract the gregorian calendar dates.
        # Example: "Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798, 1 p. in-8 obl. 22"
        if loose_gregorian_calendar_pattern.match(desc):
            # First, we start reducing the string with a first split using the comma as delimiter, as (usually) there
            # is no comma in a date:
            # ['Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798', ' 1 p. in-8 obl. 22']
            tokenizedDesc = desc.split(",")
            string_list = []
            for item in tokenizedDesc:
                if loose_gregorian_calendar_pattern.match(item):
                    string_list.append(item)
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
            # Then we clean the string
            date_string = re.sub(r'\s+', ' ', date_string)
            date_string = re.sub(r'\(', '', date_string)
            date_string = re.sub(r'L\. a\. s\.', '', date_string)
            # And eventually we can extract the date as a string to process it
            date = re.sub(r'^\s', '', date_string)

            gregorian_calendar_pattern = re.compile("^1[0-9][0-9][0-9]$")  # this pattern matches strings that contains
            # only a year

            # If the date is a year and nothing else, no need to process it.
            if gregorian_calendar_pattern.match(date):
                pass
            else:
                parsed_date = dateparser.date.DateDataParser().get_date_data(u'%s' % date)
                if parsed_date["date_obj"] is None:  # if it doesn't work, we select the YYYY string.
                    date = re.search(r"1[0-9][0-9][0-9]", date).group(0)
                else:
                    # We get the precision of the date: dateparser will autocomplete
                    # the date using the current date if it has only the month. That is not what we want.
                    if parsed_date["period"] == "month":
                        date = parsed_date["date_obj"].strftime('%Y-%m')
                    elif parsed_date["period"] == "year":  # this statement should never be true
                        date = parsed_date["date_obj"].strftime('%Y')
                    else:
                        date = parsed_date["date_obj"].strftime('%Y-%m-%d')
            dict_values["date"] = date

        # If we do not match a gregorian year string (YYYY), but a republican year string ('an V', for instance),
        # we convert the republican date
        elif republican_calendar_pattern.match(desc):
            date = rep_greg_conversion.main(desc)
            dict_values["date"] = date
        else:
            dict_values["date"] = "none"
            no_date_trigger()

        dict_values["price"] = input_dict.get(id).get("price")
        output_dict[id] = dict_values

    return output_dict

def isInt(string):
    try:
        int(string)
        return True
    except:
        return False


def is_roman(value):
    try:
        value in roman_to_arabic.keys()
        value = roman_to_arabic[value]
        return value
    except:
        return value


def pn_extractor(descList, input_dict):
    page_number_pattern = re.compile(".*[0-9\/]{0,4} p\s?[0-9\/]{0,3}.*")
    for item in descList:
        id = item[1]
        desc = item[0]
        desc = desc.translate({ord(','): ord(' '), ord('.'): ord(' ')})
        desc = re.sub(r"\s+", " ", desc)
        desc = desc.replace("p/", "p")
        dict_values = {"desc": input_dict[id].get("desc")}
        page_number = "not yet"
        if page_number_pattern.match(desc):
            pn_search = re.search("([IVXivx0-9\/]{0,6}) p\s?([0-9\/]{0,3})", desc)
            first_group = pn_search.group(1)
            second_group = pn_search.group(2)
            if pn_search.groups()[1] == '': # if the second group is empty, there is no fraction
                if first_group != '':
                    if isInt(first_group):
                        pass
                    else:
                        page_number = int(fractions_to_float[first_group])
            elif pn_search.groups()[0] != '' and pn_search.groups()[1] != '':
                if isInt(pn_search.group(1)):
                    value_1 = int(pn_search.group(1))
                else:
                    value_1 = is_roman(pn_search.group(1)) # the price
                    # can be in roman numbers
                    if isInt(value_1):
                        pass
                    else:
                        value_1 = fractions_to_float[value_1]
                if isInt(pn_search.group(2)):
                    value_2 = int(pn_search.group(2))
                else:
                    value_2 = fractions_to_float[second_group]
                page_number = float(value_1) + float(value_2)
            else:
                page_number = "TBD"
        print("%s: ; desc: %s; p1: [%s] p2: [%s]. pn: %s" % (id, desc, pn_search.group(1), pn_search.group(2), page_number))
        dict_values["number_of_pages"] = page_number
        dict_values["date"] = input_dict.get(id).get("date")
        dict_values["price"] = input_dict.get(id).get("price")
        output_dict[id] = dict_values
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
                i = clean_text(i.text)
                id = id[0]
                list_desc.append([i, id])
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
    input_text = re.sub('\(', '', input_text)
    input_text = re.sub('\)', '', input_text)
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
    # print("Total number of tei:desc elements: %s" % len(list_desc))
    output_dict = price_extractor(list_desc)
    # print("Lenght of the dictionnary (prices): %s" % len(output_dict.keys()))
    output_dict = date_extractor(list_desc, output_dict)
    # print("Lenght of the dictionnary (prices + dates): %s" % len(output_dict))
    output_dict = pn_extractor(list_desc, output_dict)
    # output_dict = format_extractor(list_desc, output_dict)

    with open('../json/export.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(output_dict, outfile)
    print("Number of entries without price: %s" % str(no_price))
    print("Number of entries without date: %s" % str(no_date))
