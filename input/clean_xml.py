#!/usr/bin/python
# coding: utf-8

# -----------------------------------------------------------
# Katabase project: github.com/katabase/
# Code by: Simon Gabay (simon.gabay[at]unige.ch)
# Python script cleaning with regex the content of XML files produced with GROBID
# Two different types of input:
#  * single file with -f parameter
#  * whole directory with -d parameter
# -----------------------------------------------------------

import glob, re, sys, getopt, os.path, argparse
from lxml import etree
from pathlib import Path

def get_new_name(input_filename,input_dirname):
      # :param input_name: name of the file
      # :return: new name to indicate it has been processed
      if not os.path.exists(input_dirname):
        os.makedirs(input_dirname)
      basename = os.path.basename(input_filename)
      basename_noExt = os.path.splitext(basename)[0]
      new_name = input_dirname+"/"+basename_noExt+"_clean.xml"
      return new_name

def process_file(input_file):
      # :param input_file: xml file
      # :return: same file with the desc cleaned
      my_doc = etree.parse(input_file)
      tei = {'tei': 'http://www.tei-c.org/ns/1.0'}
      root = my_doc.getroot()
      descs = my_doc.findall('.//tei:desc', namespaces=tei)
      for d in descs:
        d.text = desc_correction(d.text)
      return my_doc

def desc_correction(input_desc):
      # :param input_text: content of desc element
      # :return: same desc cleaned with regex
    #many several spaces to just one.
    #We do not use \s or [ \t] to keep the layout of the file
    input_desc = re.sub('(\w)    (\w)', r'\1 \2', input_desc)
    input_desc = re.sub('(\w)   (\w)', r'\1 \2', input_desc)
    input_desc = re.sub('(\w)  (\w)', r'\1 \2', input_desc)
    #main punctuation and space problems
        #hyphen
    input_desc = re.sub('\s?-\s?', '-', input_desc)
        #parenthesis
    input_desc = re.sub('\(\s', '(', input_desc)
    input_desc = re.sub('\s\)', ')', input_desc)
        #coma
    input_desc = re.sub(',(\d) ', r', \1 ', input_desc)
    input_desc = re.sub(';(\d) ', r'; \1 ', input_desc)
        #division
    input_desc = re.sub('\s?/\s?', r'/', input_desc)
        #...
    input_desc = re.sub('\s?\.\s?\.\s?\.\s?\.?', r'…', input_desc)
    #type of document
    input_desc = re.sub(' Let ', ' Let. ', input_desc)
    input_desc = re.sub('^Let ', 'Let. ', input_desc)
    input_desc = re.sub(' L aut', ' L. aut', input_desc)
    input_desc = re.sub('^L aut', 'L. aut', input_desc)
    input_desc = re.sub(' L sig', ' L. sig', input_desc)
    input_desc = re.sub('^L sig', 'L. sig', input_desc)
    input_desc = re.sub(' lig ', ' lig. ', input_desc)
    input_desc = re.sub(' lig,', ' lig.,', input_desc)
    input_desc = re.sub(' lig;', ' lig.;', input_desc)
    input_desc = re.sub(' sig ', ' sig. ', input_desc)
    input_desc = re.sub(' sig,', ' sig.,', input_desc)
    input_desc = re.sub(' sig;', ' sig.;', input_desc)
    input_desc = re.sub(' aut ', ' aut. ', input_desc)
    input_desc = re.sub(' aut,', ' aut.,', input_desc)
    input_desc = re.sub(' aut;', ' aut.;', input_desc)
    input_desc = re.sub('L\.?\s?a[^u]\.?\s?s\.? ', 'L. a. s. ', input_desc)
    input_desc = re.sub('L\.?\s?a\.? ', 'L. a. ', input_desc)
    input_desc = re.sub('L\.?\s?s\.? ', 'L. s. ', input_desc)
    input_desc = re.sub('D\.?\s?a[^u]\.?\s?s\.? ', 'D. a. s. ', input_desc)
    input_desc = re.sub('D\.?\s?a\.? ', 'D. a. ', input_desc)
    input_desc = re.sub('D\.?\s?s\.? ', 'D. s. ', input_desc)
    input_desc = re.sub('P\.?\s?a[^\w]\.?\s?s\.? ', 'P. a. s. ', input_desc)
    input_desc = re.sub('P\.?\s?a\.? ', 'P. a. ', input_desc)
    input_desc = re.sub('P\.?\s?s\.? ', 'P. s. ', input_desc)
    input_desc = re.sub('L\.?\s?a[^u]\.?\s?s\.?,', 'L. a. s.,', input_desc)
    input_desc = re.sub('L\.?\s?a\.?,', 'L. a.,', input_desc)
    input_desc = re.sub('L\.?\s?s\.?,', 'L. s.,', input_desc)
    input_desc = re.sub('D\.?\s?a[^u]\.?\s?s\.?,', 'D. a. s.,', input_desc)
    input_desc = re.sub('D\.?\s?a\.?,', 'D. a.,', input_desc)
    input_desc = re.sub('D\.?\s?s\.?,', 'D. s.,', input_desc)
    input_desc = re.sub('P\.?\s?a[^\w]\.?\s?s\.?,', 'P. a. s.,', input_desc)
    input_desc = re.sub('P\.?\s?a\.?,', 'P. a.,', input_desc)
    input_desc = re.sub('P\.?\s?s\.?,', 'P. s.,', input_desc)
    input_desc = re.sub('L\.?\s?a[^u]\.?\s?s\.?;', 'L. a. s.;', input_desc)
    input_desc = re.sub('L\.?\s?a\.?;', 'L. a.;', input_desc)
    input_desc = re.sub('L\.?\s?s\.?;', 'L. s.;', input_desc)
    input_desc = re.sub('D\.?\s?a[^u]\.?\s?s\.?;', 'D. a. s.;', input_desc)
    input_desc = re.sub('D\.?\s?a\.?;', 'D. a.;', input_desc)
    input_desc = re.sub('D\.?\s?s\.?;', 'D. s.;', input_desc)
    input_desc = re.sub('P\.?\s?a[^\w]\.?\s?s\.?;', 'P. a. s.;', input_desc)
    input_desc = re.sub('P\.?\s?a\.?;', 'P. a.;', input_desc)
    input_desc = re.sub('P\.?\s?s\.?;', 'P. s.;', input_desc)
    #Format
    input_desc = re.sub(' in-?\s?([0-9]+)°? ', r' in-\1 ', input_desc)
    input_desc = re.sub(' in-?\s?([0-9]+)°?$', r' in-\1', input_desc)
    input_desc = re.sub(' in-?\s?([0-9]+)°?\.', r' in-\1.', input_desc)
    input_desc = re.sub(' in-?\s?([0-9]+)°?,', r' in-\1,', input_desc)
    input_desc = re.sub(' in-?\s?([0-9]+)°?;', r' in-\1;', input_desc)
    input_desc = re.sub(' in-?\s?f°? ', ' in-f. ', input_desc)
    input_desc = re.sub(' in-?\s?f°?$', ' in-f.', input_desc)
    input_desc = re.sub(' in-?\s?f°?,', ' in-f.,', input_desc)
    input_desc = re.sub(' in-?\s?f°?;', ' in-f.;', input_desc)
    input_desc = re.sub(' in-?\s?f°?\.', ' in-f.', input_desc)
    input_desc = re.sub(' in-?\s?fol°? ', ' in-fol. ', input_desc)
    input_desc = re.sub(' in-?\s?fol°?$', ' in-fol.', input_desc)
    input_desc = re.sub(' in-?\s?fol°?,', ' in-fol.,', input_desc)
    input_desc = re.sub(' in-?\s?fol°?;', ' in-fol.;', input_desc)
    input_desc = re.sub(' in-?\s?fol°?\.', ' in-fol.', input_desc)
    #some abreviation signs forgotten
    input_desc = re.sub(' obl ', ' obl. ', input_desc)
    input_desc = re.sub(' obl,', ' obl.,', input_desc)
    input_desc = re.sub(' obl;', ' obl.;', input_desc)
    input_desc = re.sub(' fr ', ' fr. ', input_desc)
    input_desc = re.sub(' fr,', ' fr.,', input_desc)
    input_desc = re.sub(' fr;', ' fr.;', input_desc)
    input_desc = re.sub(' pl ', ' pl. ', input_desc)
    input_desc = re.sub(' pl,', ' pl.,', input_desc)
    input_desc = re.sub(' pl;', ' pl.;', input_desc)
    input_desc = re.sub(' Acad ', ' Acad. ', input_desc)
    input_desc = re.sub('\'Acad ', '\'Acad. ', input_desc)
    input_desc = re.sub(' (\d+) p ', r' \1 p. ', input_desc)
    input_desc = re.sub(' (\d+) p,', r' \1 p.,', input_desc)
    input_desc = re.sub(' (\d+) p;', r' \1 p.;', input_desc)
    #transforming weird prices (1 50) into decimal numbers (1.50)
    input_desc = re.sub(' (\d)\s(\d\d?)$', r' \1.\2', input_desc)
    input_desc = re.sub(' (\d\d)\s(\d\d?)$', r' \1.\2', input_desc)
    input_desc = re.sub(' (\d\d\d)\s(\d\d?)$', r' \1.\2', input_desc)

    return input_desc

if __name__ == "__main__":
    #Get value of parameter
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="add file name please")
    parser.add_argument("-d", "--dirname", help="add file name please")
    if len(sys.argv)==1:
      sys.exit("""please indicate either
        * the name of the file with -f NAME_OF_FILE
        * the name of the folder with -d NAME_OF_FOLDER""")
    args = parser.parse_args()

    #if we process only a file
    if args.filename is not None:
      #check if file exists
      if not os.path.isfile(args.filename):
        print("The File does not exit ")
        sys.exit(1)
      #create directory to put the new data
      new_dirname='Data_clean'
      new_name = get_new_name(args.filename,new_dirname)
      my_doc = process_file(args.filename)
      #save result
      my_doc.write(new_name, encoding='utf-8')

    #if we process an entire folder
    if args.dirname is not None:
      #check if directory exists
      if not os.path.isdir(args.dirname):
        print("The Directory does not exit ")
        sys.exit(1)
      #create directory to put the new data
      directory_name = args.dirname
      new_dirname=directory_name+"_clean"
      #loop over files in directory
      for file in glob.iglob(directory_name+'/*.xml'):
        new_name = get_new_name(file,new_dirname)
        my_doc = process_file(file)
        #save result
        my_doc.write(new_name, encoding='utf-8')
