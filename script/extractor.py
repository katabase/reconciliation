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




def price_extractor(descList):
    """
    Extracts the prices of the manuscripts sold and described in the tei:desc.
    :param descList: the list containing all of the tei:desc
    :return: a dict with the ids as keys, and value another dict with the prices
    """
    print("Extracting price information")
    output_dict = {}
    for item in descList:
        desc, id = item[0], item[1]
        pre_extracted_price = item[-1]
        if pre_extracted_price is not None:
            pattern = re.compile("[0-9]{0,3}\.[0-9]{0,2}")
            if pattern.match(item[-1]):
                try:
                    price = float(item[-1])
                except Exception as e:
                    add_to_log(id, e)
                    price = None
            else:
                try:
                    price = int(item[-1])
                except Exception as j:
                    add_to_log(id, j)
                    price = None
        else:
            price = None
        desc = clean_text(desc)
        dict_values = {"desc": desc}
        dict_values["price"] = price
        dict_values["author"] = item[2]
        desc_xml = desc
        output_dict[id] = dict_values
        item[0] = desc_xml
    return (output_dict)


# Second, the Extracting the date
def date_extractor(descList, input_dict):
    """
    Extracts the dates from the list containing all of the tei:desc, and update the main dict.
    :param descList: the list containing all of the tei:desc
    :param input_dict: the dictionnary containing the data previously extracted (at this moment, only the price)
    :return: a dict which keys are the ids, and which values are another dict with prices and dates
    """
    print("Extracting date information")
    for item in descList:
        desc, id = item[0], item[1]
        desc = clean_text(desc)
        loose_gregorian_calendar_pattern = re.compile(
            ".*(1[0-9][0-9][0-9]).*")  # we search for any series of four digits
        republican_calendar_pattern = re.compile(
            ".*\san ([XIVxiv]{1,4}|[0-9]{1,2}).*")  # we search for any hint of the republican calendar (in
        # general, "an" and a year in roman)
        dict_values = input_dict[id]
        date_# log_path = None
        date_range = None
        desc_xml = desc
        # Let's extract the gregorian calendar dates.
        # Example: "Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798, 1 p. in-8 obl. 22"
        if loose_gregorian_calendar_pattern.match(desc):
            date_# log_path = 1
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
            unprocessed_date_string = date_string

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

            desc_xml = desc.replace(unprocessed_date_string, f'<date xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 '
                                                             f'when=\u0022{date}\u0022>{unprocessed_date_string}</date>')

            gregorian_year_pattern = re.compile("^1[0-9][0-9][0-9]$")  # this pattern matches strings that contains
            # only a year

            # If the date is a year and nothing else, no need to process it.
            if gregorian_year_pattern.match(date):
                date_# log_path = 2
                matched = re.finditer(gregorian_year_pattern, date)
                for match in matched:
                    desc_xml = desc.replace(match.group(0), f'<date \
                           xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 when=\u0022{date}\u0022>{match.group(0)}</date>')

            else: # we are going to use the dateparser library to extract the date automatically.
                # see https://dateparser.readthedocs.io/en/v0.2.1/_modules/dateparser/date.html
                # This is the case where I could not find a way to retrieve the date string.
                date_# log_path = 3
                split_date = date.replace("(", "").replace(")", "").replace("[", "").split(" ")

                parsed_date = dateparser.date.DateDataParser().get_date_data(u'%s' % date)
                if parsed_date["date_obj"] is None:  # if it doesn't work, we select the YYYY string.
                    date_# log_path = 4
                    date = re.search("(1[0-9][0-9][0-9])", date).group(0)
                else:
                    date_range = re.search("(1[0-9][0-9][0-9])", date).span()
                    date_# log_path = 5
                    # We get the precision of the date: dateparser will autocomplete
                    # the date using the current date if it has only the month. That is not what we want.
                    if parsed_date["period"] == "month":
                        date = parsed_date["date_obj"].strftime('%Y-%m')
                    elif parsed_date["period"] == "year":  # this statement should never be true
                        date = parsed_date["date_obj"].strftime('%Y')
                    else:
                        date = parsed_date["date_obj"].strftime('%Y-%m-%d')
            # print(desc_xml)
            dict_values["date"] = date

        # If we do not match a gregorian year string (YYYY), but a republican year string ('an V', for instance),
        # we convert the republican date
        elif republican_calendar_pattern.match(desc):
            date_# log_path = 6
            date, date_string = rep_greg_conversion.main(desc)
            if date_string is not None:
                desc_xml = desc.replace(date_string, f'<date xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 date=\u0022{date}\u0022'
                                                     f' type=\u0022length\u0022>{date_string}</date>')
            else:
                desc_xml = desc
            dict_values["date"] = date
            dict_values["desc_xml"] = desc_xml
        else:
            dict_values["date"] = None
            no_date_trigger()
            desc_xml = desc
        # dict_values["date_range"] = date_range
        input_dict[id] = dict_values
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
        value in conversion_tables.roman_to_arabic.keys()
        value = conversion_tables.roman_to_arabic[value]
        return value
    except:
        return value


def length_extractor(descList, input_dict):
    print("Extracting length information")
    length_pattern = re.compile(
        "([IVXivx0-9\/]{1,6})\.?\s(pages|page|pag.|p.)\s([0-5\/]{0,3})")  # this pattern works with the most frequent cases.
    pattern_fraction = re.compile("([0-9\/]{1,6})\s?de\s?p[ages]{0,3}\.?")
    for item in descList:
        desc, id = item[0], item[1]
        desc = clean_text(desc)
        desc = re.sub(r"\s+", " ", desc)
        desc = desc.replace("p/", "p")
        dict_values = input_dict[id]
        # log_path = None
        length = None
        if re.search(length_pattern, desc):
            position_chaîne = re.search(length_pattern, desc).span()
            pn_search = re.search(length_pattern, desc)
            first_group = pn_search.group(1)
            second_group = pn_search.group(3)
            if second_group == "":  # if the second group is empty, there is no fraction
                if first_group != "":
                    if isInt(is_roman(first_group.upper())):
                        length = int(is_roman(first_group.upper()))
                        # log_path = 1
                    else:
                        try:
                            length = conversion_tables.fractions_to_float[first_group]
                            # log_path = 2
                        except:
                            length = f'key error, please check the transcription: {first_group}'
                            # log_path = 3
            elif first_group != "" and second_group != "":
                if isInt(first_group):
                    value_1 = int(first_group)
                    # log_path = 4
                else:
                    value_1 = is_roman(first_group.upper())  # the price
                    # can be in roman numbers
                    # log_path = 5
                    if isInt(value_1):
                        # log_path = 6
                        pass
                    else:
                        try:
                            value_1 = conversion_tables.fractions_to_float[value_1]
                            # log_path = 7
                        except:
                            value_1 = 501
                            # log_path = 8
                if isInt(second_group):
                    value_2 = int(second_group)
                    # log_path = 9
                else:
                    try:
                        value_2 = conversion_tables.fractions_to_float[second_group]
                        # log_path = 10
                    except:
                        value_2 = 404
                        # log_path = 11
                length = float(value_1) + float(value_2)
            else:
                length = None
                # log_path = 12
        elif re.search(pattern_fraction, desc):
            # log_path = 13
            search = re.search("([0-9\/]{1,6})\s?de\s?p[age]{0,3}\.?", desc)
            position_chaîne = search.span()
            try:  # test to be removed after.
                length = conversion_tables.fractions_to_float[search.group(1)]
            except:
                length = 0

        if length != None:
            starting_position = position_chaîne[0]
            ending_position = position_chaîne[1]
            if desc[ending_position - 1] == " ":  # if a space is the last character of the identified range of page ("1 p. "), we can
                ending_position = ending_position - 1
            desc_xml = f'{desc[:starting_position]}<measure xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022' \
                       f' type=\u0022length\u0022 unit=\u0022p\u0022 n=\u0022{length}\u0022>' \
                       f'{desc[starting_position:ending_position]}</measure>{desc[ending_position:]}'
        else:
            desc_xml = desc
        # dict_values["path"] = path  # idem # for debugging purposes only
        dict_values["number_of_pages"] = length
        input_dict[id] = dict_values
        item[0] = desc_xml
    return input_dict


def format_extractor(descList, input_dict):
    print("Extracting format information")
    for item in descList:
        desc, id = item[0], item[1]
        desc_xml = desc
        ms_format = None
        dict_values = input_dict[id]
        format_simple_pattern = re.compile("(in-[0-9]{1,2}°?\.?\s?[obl]{0,3}\.?)")
        format_simple_pattern2 = re.compile("(in-folio\.?\s?[obl]{0,3}\.?)")
        format_simple_pattern3 = re.compile("(in-f[ol]{0,2}\.?\s?[obl]{0,3}\.?)")

        if re.search(format_simple_pattern, desc):
            format_search = re.search(format_simple_pattern, desc)
            ms_format = re.sub(r"\s$", "", format_search.group(1))
            position = format_search.span()
            start_position = position[0]
            end_position = position[1]

        elif re.search(format_simple_pattern2, desc):
            format_search = re.search(format_simple_pattern2, desc)
            ms_format = re.sub(r"\s$", "", format_search.group(1))
            position = format_search.span()
            start_position = position[0]
            end_position = position[1]

        elif re.search(format_simple_pattern3, desc):
            format_search = re.search(format_simple_pattern3, desc)
            ms_format = re.sub(r"\s$", "", format_search.group(1))
            position = format_search.span()
            start_position = position[0]
            end_position = position[1]
        else:
            desc_xml = desc
            start_position = None
            end_position = None


        # dict_values["desc_xml"] = desc_xml
        # let's improve the format identification
        obl_pattern = re.compile(".*ob[l]{0,1}.*")
        format_pattern = re.compile("(in-[0-9]{1,2})")
        fol_pattern = re.compile(".*in\-f[olio]?.*")
        if ms_format is not None:
            if re.search(fol_pattern, ms_format):
                encoded_ms_format = 1
            elif re.search(format_pattern, ms_format):
                encoded_ms_format = re.search(format_pattern, ms_format).group(1)
                try:
                    encoded_ms_format = conversion_tables.format_types[encoded_ms_format]
                except:
                    encoded_ms_format = None
            else:
                encoded_ms_format = None

            if encoded_ms_format is not None:
                if re.search(obl_pattern, ms_format):
                    encoded_ms_format = encoded_ms_format + 100

        # Let's create the xml element
        if start_position and end_position:
            if desc[end_position - 1] == " ":  # if the last character of the identified format is a space
                end_position = end_position - 1
            desc_xml = f"{desc[:start_position]}<measure xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 " \
                       f" type=\u0022format\u0022 unit=\u0022f\u0022 n=\u0022{encoded_ms_format}\u0022>" \
                       f"{desc[start_position:end_position]}</measure>{desc[end_position:]}"
            # desc_xml = desc

        dict_values["desc_xml"] = desc_xml
        dict_values["format"] = encoded_ms_format
        input_dict[id] = dict_values
        item[0] = desc_xml # we update the list
    return input_dict


def term_extractor(descList, input_dict):
    print("Extracting term information")
    for item in descList:
        desc, id, author, sell_date = item[0], item[1], item[2], item[3]
        desc_xml = desc
        term = None
        dict_values = input_dict[id]

        apas_pattern = re.compile("((Apostille)\s?a[utographe]{0,9}\.?\s?[signée]{0,6}\.?)")  # > Apas
        pas_pattern = re.compile("(([Pp]ièce|[Pp]\.)\s[^<]*?au[tographe]{1,8}\.?\s?si[gnée]{0,4}\.?)")  # > Pas
        pa_pattern = re.compile("(([Pp]ièce|[Pp]\.)(?!<)\s?[^<]*aut[ographe]{0,7}\.?)")  # > Pa
        ps_pattern = re.compile("(([Pp]ièce|[Pp]\.)\s?(signée|sig|sig\.|s\.))")  # > Ps
        bias_pattern = re.compile("((Billet|B\.)\s?a[utographe]{0,9}\.?\s?s[igné]{0,4}\.?)")  # > bias
        bis_pattern = re.compile("((Billet|B\.)\s?s[igné]{0,4}\.?)")  # > bis
        las_pattern = re.compile("((Lettre|Let\.|L\.)\s?a[utographe]{0,9}\.?\s?s[ignée]{0,5}\.?)")  # > Las
        la_pattern = re.compile("((Lettre|Let\.|L\.) a[utographe]{0,9}\.?)")  # > La
        ls_pattern = re.compile("((Lettre|Let\.|L\.) (signée|sig\.|s\.))")  # > Ls
        brs_pattern = re.compile("(Brevet\.?\s?[signé]{0,5}\.?)")  # > Brs
        qas_pattern = re.compile("(Quitt[ance]{0,4}?\.?\s?[autographe]{0,10}\.?\s?[signée]{0,6}\.?)")  # > Qas
        qs_pattern = re.compile("(Quitt[ance]{0,4}?\.?\s?[signée]{0,6}\.?)")  # > Qs
        ma_pattern = re.compile("([Mm]anuscrit aut[ographe]{0,7}\.?)")  # > Ma
        ca_pattern = re.compile("([Cc]hanson\saut[ographe]{0,7}\.?)")  # > Ca
        as_pattern = re.compile(
            "((Autographe|autographe|[Aa]ut\.|[Aa]\.)\s?s[ignée]{0,5}\.?)")  # > as # this one must be the last pattern tested.

        if re.search(pas_pattern, desc):
            term_search = re.search(pas_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["P.a.s."]
            
            correct_pattern = pas_pattern

        elif re.search(apas_pattern, desc):
            term_search = re.search(apas_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["Ap.a.s."]
            
            correct_pattern = apas_pattern


        elif re.search(ps_pattern, desc):
            term_search = re.search(ps_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["P.s."]
            
            correct_pattern = ps_pattern

        elif re.search(pa_pattern, desc):
            term_search = re.search(pa_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["P.a."]
            
            correct_pattern = pa_pattern


        elif re.search(bias_pattern, desc):
            term_search = re.search(bias_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["Bi.a.s."]
            
            correct_pattern = bias_pattern

        elif re.search(bis_pattern, desc):
            term_search = re.search(bis_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["Bi.s."]
            
            correct_pattern = bis_pattern


        elif re.search(las_pattern, desc):
            term_search = re.search(las_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["L.a.s."]
            
            correct_pattern = las_pattern

        elif re.search(la_pattern, desc):
            term_search = re.search(la_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["L.a."]
            
            correct_pattern = la_pattern

        elif re.search(brs_pattern, desc):
            term_search = re.search(brs_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["Br.s."]
            
            correct_pattern = brs_pattern

        elif re.search(qs_pattern, desc):
            term_search = re.search(qs_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["Q.s."]
            
            correct_pattern = qs_pattern

        elif re.search(ma_pattern, desc):
            term_search = re.search(ma_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["M.a."]
            
            correct_pattern = ma_pattern

        elif re.search(ca_pattern, desc):
            term_search = re.search(ca_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["C.a."]
            
            correct_pattern = ca_pattern

        elif re.search(qas_pattern, desc):
            term_search = re.search(qas_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["Q.a.s."]
            
            correct_pattern = qas_pattern

        elif re.search(ls_pattern, desc):
            term_search = re.search(ls_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["L.s."]
            
            correct_pattern = ls_pattern

        elif re.search(as_pattern, desc):  # keep this search the last one
            term_search = re.search(as_pattern, desc)
            term = re.sub(r"\s$", "", term_search.group(1))
            norm_term = conversion_tables.term_types["A.s."]
            
            correct_pattern = as_pattern

            # Check this problem (not matched by as_pattern):
            # "CAT_000096_e249": {
            #     "desc": "Rome, 20 juillet 1691; aut. sig. – 7 pag. – A M. de Lamoignon, avocat-général. (Très-curieuse.)",
            #     "price": null,
            #     "desc_xml": "Rome, 20 juillet 1691; aut. sig. – <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"7\" type=\"length\">7 pag.</measure> – A M. de <term xmlns=\"http://www.tei-c.org/ns/1.0\" type=\"format\">La</term>moignon, avocat-général. (Très-curieuse.)",
            #     "date": "1691-07-20",
            #     "number_of_pages": 7,
            #     "format": null,
            #     "term": "La"
            # },

        else:
            desc_xml = desc
            norm_term = None
            correct_pattern = None

        # Let's create the xml element
        if correct_pattern:
            desc_xml = desc.replace(term, f'<term xmlns=\u0022http://www.tei-c.org/ns/1.0\u0022 '
                                                         f'type=\"{norm_term}\">{term}</term>')
        dict_values["desc_xml"] = desc_xml
        dict_values["term"] = norm_term
        dict_values["author"] = author
        dict_values["sell_date"] = sell_date
        input_dict[id] = dict_values
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
    This function extracts from an xml file all of the tei:desc elements
    :return: a list of lists that contains the tei:desc value, the date of the sale,
    """
    with open(input, 'r+') as fichier:
        tei = {'tei': 'http://www.tei-c.org/ns/1.0'}
        f = etree.parse(fichier)
        root = f.getroot()
        desc = root.xpath("//tei:desc", namespaces=tei)
        list_desc = []
        sell_date = root.xpath("//tei:sourceDesc//tei:date", namespaces=tei)[0].text
        for i in desc:
            author = i.xpath("parent::tei:item/tei:name", namespaces=tei)
            try:
                price = i.xpath("parent::tei:item//tei:measure[@commodity='currency']/@quantity", namespaces=tei)[0]
            except:
                price = None
            id = i.xpath("@xml:id", namespaces=tei)
            if len(id) > 0:  # some of the tei:item do not contain any identifier. We ignore them.
                id = id[0]
                if len(author) > 0:
                    author = author[0].text
                    try:
                        author = author.split(" ")[0]# we keep only the surname of the author
                        list_desc.append([i.text, id, author,  sell_date, price])
                    except:
                        author = None
                        list_desc.append([i.text, id, author,  sell_date, price])
                else:
                    author = None
                    list_desc.append([i.text, id, author, sell_date, price])
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
    """
    This function creates a global list gathering all tei:desc from the xml files.
    :param path:date
    :return:
    """
    final_list = []
    for xml_file in glob.iglob(path):
        for desc_element in desc_extractor(xml_file):
            final_list.append(desc_element)
    return final_list


def xml_output_production(dictionnary):
    """
    Replaces all tei:desc by the structure
    :param dictionnary: the dictionnary created by the different extraction steps
    :return:
    """
    print("Updating the xml files")
    tei_namespace = "http://www.tei-c.org/ns/1.0"
    NSMAP1 = {'tei': tei_namespace}  # pour la recherche d'éléments avec la méthode xpath
    ElementTree.register_namespace("", tei_namespace)  # http://effbot.org/zone/element-namespaces.htm#preserving
    # -existing-namespace-attributes
    for key in dictionnary:
        input_info = key.split("_")
        file = f'{input_info[0]}_{input_info[1]}_clean.xml'  # the filename follow the structure CAT_ID.xml
        item = input_info[2].split("e")[-1]
        desc_string = output_dict[key]["desc_xml"].replace("&", "&amp;")
        input_file = f'../output/xml/{file}'
        try:
            with open(input_file, 'r+') as fichier:
                f = etree.parse(fichier)
                output_root = f.getroot()
                # log_path = f'//tei:item[@n=\'{item}\']/tei:desc'
                desc_list = output_root.xpath(path, namespaces=NSMAP1)
                for desc in desc_list:  # now let's update the tei:desc elements in the output file
                    item_element = desc.getparent()  # https://stackoverflow.com/questions/7474972/python-lxml-append
                    # -element-after-another-element
                    try:
                        item_element.insert(item_element.index(desc) + 1, etree.fromstring("<desc xmlns=\"http://www.tei-c.org/ns/1\">%s</desc>" % desc_string))
                    except Exception as e:
                        add_to_log('no_id', e, desc_string)
                    item_element.remove(desc)  # we remove the non processed tei:desc
                output_file = f'../output/xml/{file}'
                with open(output_file, "w+") as sortie_xml:
                    output = etree.tostring(output_root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode(
                        'utf8')
                    sortie_xml.write(str(output))
        except Exception as e:
            add_to_log(key, e)

def add_to_log(id, exception, *args):
    """
    This function creates a log file with the entries that are not correctly formatted
    :param id: the identifier of the incorrect entry
    :param exception: the exception raised
    :param args: other problems
    :return: None
    """
    exception = str(exception)
    with open('log.log', 'a') as log_file:
        log_file.write(f'\n {id} throws and error \n {exception}')
        if args:
            log_file.write(f'\n Additional information:\n {str(args)}')



def duplicates_identification(a):
    seen = {}
    dupes = []
    for x in a:
        if x not in seen:
            seen[x] = 1
        else:
            if seen[x] == 1:
                dupes.append(x)
            seen[x] += 1
    return dupes

if __name__ == "__main__":
    no_price = 0
    no_date = 0
    with open('log.log', 'w') as log_file:
        log_file.truncate(0)
    files = "../input/Data_clean/*5_clean.xml"
    input_dir = os.path.dirname(files)
    output_dir = "../output/xml"
    try:
        shutil.copytree(input_dir, output_dir)  # shutil.copytree contains a mkdir command, we have to delete the
        # directory if it exists
    except:
        shutil.rmtree(output_dir)
        shutil.copytree(input_dir, output_dir)
    list_desc = conversion_to_list(files)
    output_dict = price_extractor(list_desc)
    output_dict = date_extractor(list_desc, output_dict)
    output_dict = length_extractor(list_desc, output_dict)
    output_dict = format_extractor(list_desc, output_dict)
    output_dict = term_extractor(list_desc, output_dict)


    xml_output_production(output_dict)

    for key in output_dict:
        del output_dict[key]["desc_xml"]

    with open('../output/json/export.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(output_dict, outfile)


    print("Done !")
    # print(f'Number of entries without price: {str(no_price)}')
    # print(f'Number of entries without date: {str(no_date)}')
