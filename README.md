# OPERATION RECONCILIATION

Reconciliation of manuscript sale catalogues entries

# 1. Objective
Manuscript sale catalogues propose list of manuscript for sale. A same manuscript can be sold multiple times.

<img src="README/1894_05_RDA_N166_14_sev.jpeg" width="20%" align="middle"><img src="README/1897_07_RDA_N200_16_sev.jpeg" width="30%" align="middle"><img src="README/1902_04_RDA_N257_13_sev.jpeg" width="30%" align="middle">


Our objective is to detect such similar entries.

# 2. Workflow

## 2.1. Cleaning of the data

Entries of catalogues look like the following:

```xml
<item n="80" xml:id="CAT_000146_e80">
   <num>80</num>
   <name type="author">Cherubini (L.),</name>
   <trait>
      <p>l'illustre compositeur</p>
   </trait>
   <desc>L. a s.; 1836, 1 p 1 /2 in8.</desc>
    <measure commodity="currency" unit="FRF" quantity="3">12</measure>
</item>
```

Most of the reconciliation process uses data from the `<desc>` element of our xml files. We therefore need to correct typos to ease further post-processing, _e.g._
  * `L. a s.` -> `L. a. s.`
  * `in8` -> `in-8`
  * `1 /2` -> `1/2`
  * `1 p ` -> `1 p. `

The `clean-xml.py` script [[available here](https://github.com/katabase/reconciliation/tree/master/input)] tackles this problem:

  * `python clean-xml.py -f FILENAME` processes one single file
  * `python clean-xml.py -d DIRECTORY` processes all the files contained in a directory

## 2.2. Information retrieval in the `desc`

We need to extract data from the `desc` and transform

```xml
<item n="80" xml:id="CAT_000146_e80">
   <num>80</num>
   <name type="author">Cherubini (L.),</name>
   <trait>
      <p>l'illustre compositeur</p>
   </trait>
   <desc>L. a. s.; 1836, 1 p. in-8.</desc>
    <measure commodity="currency" unit="FRF" quantity="3">12</measure>
</item>
```

into

```json
{
"CAT_000156_e14_d1": {
    "desc": "L. a. s.; 1836, 1 p. in-8. 12",
    "price": 12,
    "author": "Cherubini",
    "date": 1836,
    "number_of_pages": 1,
    "format": 8,
    "term": 4,
    "sell_date": "Mars 1893"
  }
}
```

and

```xml
<item n="80" xml:id="CAT_000146_e80">
   <num>80</num>
   <name type="author">Cherubini (L.),</name>
   <trait>
      <p>l'illustre compositeur</p>
   </trait>
   <desc><term>L. a. s.</term>;<date>1836</date>,
   <measure type="length">1 p.</measure> <measure type="length">in-8</measure>.
   <measure commodity="currency" unit="FRF" quantity="3">12</measure></desc>
</item>
```
(xml output not fully implemented)

### 2.3 Reconciliation of the entries






### Installation 

To carry this task we use the `extractor.py` and the `reconciliator.py` [[available here](https://github.com/katabase/reconciliation/tree/master/script)].

```
git clone https://github.com/katabase/reconciliation.git
cd reconciliation
python3 -m venv my_env
source my_env/bin/activate
pip3 install -r requirements.txt
```

### Using the tool

Two main scripts are used: 
+ the first one, `extractor.py`, is for the extraction of the information in the xml files
+ the second one, `reconciliator.py`, is used to reconciliate the entries, *i.e.* to identify the entries corresponding 
to the same documents. The user has to provide an author  (using the flag `-a`) to filter the database. The user can also 
filter by date (using the flag -d). 

The data will be stored in json in folders corresponding to the date and the authorname. Three files are created: 
+ `filtered_db.json` is the result of the extraction before the reconciliation of the entries.
+ `reconciliated_pairs.json` provides a list of all the *probable* similar documents, ordered by probability
+ `reconciliated_documents.json` provides the list of the documents that have been reconciliated.
+ `final_db.json` contains all the entries with the reconciliation done 


#### First example

We want to work on Mme de Sévigné. 
+ First, we create the database. In the script directory, ``python3 extractor.py``
+ Then, we use the second script: ``python3 reconciliator.py -a Sévigné``
+ The files will be stored in ``output/json/Sevigne/``

#### Second example
We want to select the production of Mme de Sévigné between 1680-1690: 
+ First, we create the database. In the script directory, ``python3 extractor.py``
+ Then, we use the second script with the -d flag: ``python3 reconciliator.py -a Sévigné -d 1680-1690``
+ The results will be stored in `output/json/Sevigne/1680-1690/`

### Cite this repository
If you use these data, please cite this paper:
```
@inproceedings{gabay:howmanyDH2020,
  AUTHOR = {Gabay, Simon and Rondeau Du Noyer, Lucie and Gille Levenson, Matthias, and Petkovic, Ljudmila, and Bartz, Alexandre},
  TITLE = {Quantifying the Unknown. How many manuscripts of the marquise de Sévigné still exist?},
SHORTTITLE = {Quantifying the Unknown},
  ADDRESS = {Ottawa, Canada},
  MONTH = July,
  YEAR = {2020},
  BOOKTITLE = {DH2020: carrefours/intersections},
  KEYWORDS = {Machine learning ; Manuscript sales catalogues ; 19th c. France; Mme de Sévigné},
}
```

### Licence
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Licence Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution 4.0 International Licence</a>.
