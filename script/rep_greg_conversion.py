import json
import re
from conversion_tables import *


with open("../json/corresp_table.json", "r") as corresp_table:
    conversion_table = json.load(corresp_table)

def is_int(string):
    pattern = re.compile("[0-9]{1,3}")
    if pattern.match(string):
        return True
    else:
        return False


def full_conversion(year, month, day):
    """
    Converts a full republican date to gregorian date
    :param year:
    :param month:
    :param day:
    :return: A string of the form "YYYY-MM-DD"
    """
    if is_int(year):
        reg_year = year
    else:
        reg_year = roman_to_arabic[year]
    if day in cardinals.keys():
        reg_day = cardinals[day]
    else:
        reg_day = day
    if month in abbreviations.values():
        reg_month = month
    elif month.translate({ord(','): None, ord('.'): None}) in abbreviations.keys():
        reg_month = abbreviations[month.translate({ord(','): None, ord('.'): None})]
    else:
        reg_month = month
    day_and_month = "%s %s" % (reg_day, reg_month)
    try:
        date = conversion_table[day_and_month][str(reg_year)]
    except:
        date = "none"
    return date

def partial_conversion(year):
    """
    Converts the republican year to gregorian year
    :param year:
    :return: a string with a range of year
    """
    if is_int(year):
        reg_year = year
    else:
        reg_year = roman_to_arabic[year]
    date = year_range[str(reg_year)]
    return date


def main(desc):
    full_date = re.search("([0-3]{0,1}[0-9I][er]{0,2}) (.{0,13}) an ([XIVxiv]{1,4}|[0-9]{1,2})", desc)
    partial_date = re.search("an ([XIVxiv]{1,4}|[0-9]{1,2})", desc)
    if full_date:
        date_span = full_date.span()
        day = full_date.group(1)
        month = full_date.group(2)
        year = full_date.group(3).upper()
        date = full_conversion(year, month, day)
    elif not full_date and partial_date:
        date_span = partial_date.span()
        year = partial_date.group(1).upper()
        date = partial_conversion(year)
    else:
        date = "none"

    if date != "none":
        start_position = date_span[0]
        end_position = date_span[1]
    else:
        start_position = None
        end_position = None
    return date, start_position, end_position
