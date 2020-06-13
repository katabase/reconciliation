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
    "niv.": "nivôse",
    "fruct.": "fructidor",
    "flor.": "floréal",
    "frim.": "frimaire",
    "therm.": "thermidor",
    "brum.": "brumaire",
    "germ.": "germinal",
    "pluv.": "pluviôse",
    "prair.": "prairial",
    "vendém.": "vendémiaire",
    "vend.": "vendémiaire",
}

with open("../json/corresp_table.json", "r") as conversion_table:
    conversion_table = json.load(conversion_table)


def conversion(year, month, day, dictionnary):
    reg_year = years_conversion[year]
    if day in cardinals.keys():
        reg_day = cardinals[day]
    else:
        reg_day = day
    if month in abbreviations.values():
        reg_month = month
    elif month in abbreviations.keys():
        reg_month = abbreviations[month]
    else:
        reg_month = month
    day_and_month = "%s %s" % (reg_day, reg_month)
    print("Spotted republican date: %s %s" % (day_and_month, year))
    try:
        date = conversion_table[day_and_month][str(reg_year)]
    except:
        date = "none"
    return date



def main(desc):
    search = re.search("([0-3]{0,1}[0-9][er]{0,4}) (.{0,10}) an ([XIVxiv]{1,4})", desc)
    if search:
        day = search.group(1)
        month = search.group(2)
        year = search.group(3).upper()
        date = conversion(year, month, day, conversion_table)
        print("Spotted republican calendar. %s" % date)
    else:
        date = "none"
    return date
