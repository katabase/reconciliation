import json
import re

years_conversion = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
    "XIII": 13,
    "XIV": 14
}

year_range = {
    "1": "1792-1793",
    "2": "1793-1794",
    "3": "1794-1795",
    "4": "1795-1796",
    "5": "1796-1797",
    "6": "1797-1798",
    "7": "1798-1799",
    "8": "1799-1800",
    "9": "1800-1801",
    "10": "1801-1802",
    "11": "1802-1803",
    "12": "1803-1804",
    "13": "1804-1805",
    "14": "1805"
}

cardinals = {
    "1er": "1"
}

abbreviations = {
    "niv": "nivôse",
    "nivose": "nivôse",
    "fruct": "fructidor",
    "flor": "floréal",
    "floreal": "floréal",
    "frim": "frimaire",
    "therm": "thermidor",
    "mess": "messidor",
    "ventose": "ventôse",
    "brum": "brumaire",
    "germ": "germinal",
    "pluv": "pluviôse",
    "pluviose": "pluviôse",
    "prair": "prairial",
    "vendém": "vendémiaire",
    "vend": "vendémiaire",
    "vent": "ventôse",
}

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
        reg_year = years_conversion[year]
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
        reg_year = years_conversion[year]
    date = year_range[str(reg_year)]
    return date


def main(desc):
    full_date = re.search("([0-3]{0,1}[0-9I][er]{0,2}) (.{0,13}) an ([XIVxiv]{1,4}|[0-9]{1,2})", desc)
    partial_date = re.search("an ([XIVxiv]{1,4}|[0-9]{1,2})", desc)
    if full_date:
        day = full_date.group(1)
        month = full_date.group(2)
        year = full_date.group(3).upper()
        date = full_conversion(year, month, day)
    elif not full_date and partial_date:
        year = partial_date.group(1).upper()
        date = partial_conversion(year)
    else:
        date = "none"
    return date
