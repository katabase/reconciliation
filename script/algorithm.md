## Algorithm

- First we have to clean the tei:desc elements. 
- We start with the end of the string. We tokenize using the space as a delimiter. 
The simplest rule: **if the last token is a number, we have a price**. 
- But we have some prices that are not formated this way. For example, 
`Let.aut. sig. P. Lx; Boussac, 15 avril (1848), 2 p. 1/2 in-8.10`. 
Here, there is no space after the format of the document.  
- New rule: **if the last token ends with a dot and a number, we also have a price**.
"\.[0-999]$" 
- Another rule: ".*-6$" (in-6 does not exist), but we can't generalize 
as we would match in-4 and in-8. 
- "in-[0-10]°[0-999]"


## Possible issues with the extraction of the price
- in-4°50 (L. s. à M. Carroll ; New-York, 9 octobre 1911, 1/2 p. in-4°50)
-5 (L. a. s. à l'abbé Martin, 1833, 2 p. in-4. -5)
- (L. a. s. à l'abbe Caluso, 1788, 2 p. 1/2 in-8, cachet. 5 -)
-6 (L. a. s. (à la marquise de Créqui), 1 p. 1/2 in-4. -6)
in-8.10 (Let.aut. sig. P. Lx; Boussac, 15 avril (1848), 2 p. 1/2 in-8.10)
armoiries (Belle pièce sig. sur vélin, 1699, in-f. 2 50 
Certificat de noblesse de Th.-Ph. de Saint-Nicolas, trésorier de France au bureau
d'Alençon, avec ses armoiries)
- Quittance (Pièce sur vélin; 15 mars 1392 (1393), in-8 obl.; fragment de sceau. 50 Quittance)

## Issues in date extraction
- 1734-55 > 1734
- CAT_000086_e196:  [L. a. s.; 1825; 1 p. in-4. 2] > ø [fixed]
- CAT_000086_e171: né à Rodez en 1767 [-J.-H. de), poète distingué, né à Rodez en 1767. -1° L. a. s. à M. Déhault, 10 flor, an XII, 3 p. in-4. Légère déchirure toute relative à sa traduction de l'Enéide. -2° Sa biographie, pièce aut. de M. Villenave, 11 p. in-4. 5]
- CAT_000123_e148: Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798 [Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798, 1 p. in-8 obl. 22]
- CAT_000123_e81: L. a. s. au comte de Villèle : 14 avril 1826 [L. a. s. au comte de Villèle : 14 avril 1826, 1 p. in-fol. 15] [fixed]
- CAT_000123_e81: au comte de Villèle : 14 avril 1826 [L. a. s. au comte de Villèle : 14 avril 1826, 1 p. in-fol. 15] [fixed]
- CAT_000102_e135: Leipzig. « juin 1846 [Morceau de musique aut. sig.; Leipzig. « juin 1846, 1/2 p. in-8 obl. 15]  [fixed]
- CAT_000137_e112: "desc": "Let. aut. ; Coppet, 8'août, 2 p. 1/2 in-4. 28",date:none
- "CAT_000102_e195": {
    "desc": "L. a. s. à M. Perraut, à Lons-le-Saunier; Montaigu, 24 décembre, 1 p. in-8. 40",
    "price": "40",
    "date": "none"
  }, [do we have to extract partial date information ? would it be useful ?]
-  "CAT_000151_e138": {
    "desc": "L. a. s. à ses électeurs ; Paris, 1er oct. an Ier de de la République, 1 p. in-4. 25",
    "price": "25",
    "date": "1807"
  },
  
 ## Issues related to the Republican calendar
 -   "CAT_000053_e156": {
    "desc": "Let. sig. au Comité de Salut public; quartier-général de Figuières, 5 nov. an III, 2 p. in-4. 5",
    "price": "5",
    "date": "1879-05-31"
  }, (mix of the two calendars)
 -   "CAT_000032_e20": {
    "desc": "L. a. s. à Jos. Bonaparte; Ecouen, 1er pluv. an VII, 2 p. in-4. 25",
    "price": "25",
    "date": "none"
  }, [fixed]
 -   "CAT_000001_e77": {
    "desc": "L. aut. sig., au ministre Chaptal. 24 pluv. an xi. 2 pag. in-folio",
    "price": "none",
    "date": "none"
  },
 -   "CAT_000025_e75": {
    "desc": "L. a. s. aux administrateurs du district de Boulogne ; Calais, 15 frim. an 2, 2 p. in-4. 20",
    "price": "20",
    "date": "none"
  }, [fixed]
 -   "CAT_000123_e216": {
    "desc": "L. a. s., Paris, 26 vendémiaire an XI, 1 p. in-4. 10",
    "price": "10",
    "date": "none"
  }, [fixed: vendémiaire is more than 10 characters long]
-   "CAT_000138_e229": {
    "desc": "L. a. s., en français, au citoyen Le Roux; Paris, 21 nivôse an II 10 janvier 1794, 3 p. in-8. 12",
    "price": "12",
    "date": "1794"
  },
-   "CAT_000025_e35": {
    "desc": "L. a. s. au citoyen Flaminius Aquaronc; Toulon, 6 vent, an XI, 1 p. in-8. 10",
    "price": "10",
    "date": "none"
  }, [fixed]
-   "CAT_000046_e119": {
    "desc": "L. aut. sig. de ses initiales à l'imprimeur Agasse; 3 ventôse, 3 p. pl. in-4. 6",
    "price": "6",
    "date": "none"
  },
-   "CAT_000046_e136": {
    "desc": "L. a. s. Jacques Sutamier, à la duchesse de Saxe-Gotha; Nyon, au pays de Vaud, 15 fév., 4 p. pl. in-4. 50",
    "price": "50",
    "date": "none"
  },
-   "CAT_000104_e192": {
    "desc": "Pièce sig. sur vélin ; Nancy, 27 mars 1488 1489, 1 p. in-4 obl. 40",
    "date": "1488",
    "price": "40"
  },
    "CAT_000001_e148": {
    "desc": "Quittance aut. sig., de la somme de mille livres en l'acquit de M. le duc de Bouillon, etc. Paris, le 7 mai 1605. Demi-page in-folio.",
    "price": "none",
    "desc_xml": "Quittance aut. sig., de la somme de mille livres en l'acquit de M. le duc de Bouillon, etc. Paris, le 7 mai 1605. Demi-page in-folio.",
    "date": "1605-05-07",
    "number_of_pages": "none"
  },
  
  
## Issues with the extraction of number of pages
  "CAT_000100_e32": {
    "desc": "Let. sig. ; Lyon, 1850, 3/4 de p. in-4. 2",
    "date": "1850",
    "price": "2"
  },
  "CAT_000133_e31": {
    "desc": "Let. sig. avec la souscript. aut. à M. de Brosses, bailly de Gex ; Chamy, 21 nov. 1639, 3/4 de p. 30",
    "price": 30,
    "desc_xml": "Let. sig. avec la souscr<measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"1\" type=\"lenght\">ip</measure>t. aut. à M. de Brosses, bailly de Gex ; Chamy, <date xmlns=\"http://www.tei-c.org/ns/1.0\" date=\"1639-11-21\" type=\"lenght\">21 nov. 1639</date>, 3/4 de p. <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"30\" type=\"price\">30</measure>",
    "date": "1639-11-21",
    "number_of_pages": 1
  },
    "CAT_000100_e8": {
    "desc": "Billet à ordre signé, 1846, in-8. Curieux. 8",
    "price": 8,
    "desc_xml": "Billet à <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"none\" type=\"lenght\">ordr</measure>e signé, <date xmlns=\"http://www.tei-c.org/ns/1.0\" when=\"1846\">1846</date>, in-8. Curieux. <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"8\" type=\"price\">8</measure>",
    "date": "1846",
    "number_of_pages": "none"
  }, [fixed]
    "CAT_000001_e148": {
    "desc": "Quittance aut. sig., de la somme de mille livres en l'acquit de M. le duc de Bouillon, etc. Paris, le 7 mai 1605. Demi-page in-folio.",
    "price": "none",
    "desc_xml": "Quittance aut. sig., de la somme de mille livres en l'acquit de M. le duc de Bouillon, etc. Paris, le 7 mai 1605. Demi-page in-folio.",
    "date": "1605-05-07",
    "number_of_pages": "none"
  },
    "CAT_000143_e111": {
    "desc": "L. a. s. au ministre Windham ; (Londres), 29 janv. 1794, 1/2 p. in-4. 50",
    "price": 50,
    "desc_xml": "L. a. s. au ministre Windham ; (Londres), <date xmlns=\"http://www.tei-c.org/ns/1.0\" date=\"1794-01-29\" type=\"lenght\">29 janv. 1794</date>, <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"0\" type=\"lenght\">1/2 p. </measure>in-4. <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"50\" type=\"price\">50</measure>",
    "date": "1794-01-29",
    "number_of_pages": 0
  }, [fixed]
    "CAT_000022_e5": {
    "desc": "L. a. s., 1853. Spirituelle épître. 2 50",
    "price": 50,
    "desc_xml": "L. a. s., <date xm<measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"\" type=\"length\">lns=\"ht</measure>tp://www.tei-c.org/ns/1.0\" when=\"1853\">1853</date>. Spirituelle épître. 2 <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"50\" type=\"price\">50</measure>",
    "date": "1853",
    "path": 2,
    "number_of_pages": ""
  },[big problem] [fixed]
    "CAT_000138_e7": {
    "desc": "Pièce sig., sig. aussi par Laplaïgne; thermidor an III, 1 p. 1/2 in-fol., tête imp. 10",
    "price": 10,
    "desc_xml": "Pièce sig., sig. auss<measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"1\" type=\"length\">i p</measure>ar Laplaïgne; thermidor <date xmlns=\"http://www.tei-c.org/ns/1.0\" date=\"1794-1795\" type=\"length\">an III</date>, 1 p. 1/2 in-fol., tête imp. <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"10\" type=\"price\">10</measure>",
    "date": "1794-1795",
    "number_of_pages": 1
  }, [revoir l'identification des dates républicaines; mais dans ces dates partielles pour l'instant le mois n'est pas pris en compte]
    "CAT_000074_e7": {
    "desc": "Let. sig., avec la souscript. et un post-script, de 6 lignes aut., à M. de Rambouillet ; Lyon, 12 octobre 1574, 1 p. in-fol. Deux petites déchirures dans le texte. 20",
    "price": 20,
    "desc_xml": "Let. sig., avec la souscr<measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"1\" type=\"length\">ip</measure>t. et un post-script, de 6 lignes aut., à M. de Rambouillet ; Lyon, <date xmlns=\"http://www.tei-c.org/ns/1.0\" date=\"1574-10-12\" type=\"length\">12 octobre 1574</date>, 1 p. in-fol. Deux petites déchirures dans le texte. <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"20\" type=\"price\">20</measure>",
    "date": "1574-10-12",
    "number_of_pages": 1
  },
   "CAT_000077_e7": {
    "desc": "Let. sig., avec la souscript. aut., comme cardinal, à Albergati Capacelli; Ancône, 1731, 3/4 de p. in-4. 10",
    "price": 10,
    "desc_xml": "Let. sig., avec la souscr<measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"1\" type=\"length\">ip</measure>t. aut., comme cardinal, à Albergati Capacelli; Ancône, <date xmlns=\"http://www.tei-c.org/ns/1.0\" when=\"1731\">1731</date>, 3/4 de p. in-4. <measure xmlns=\"http://www.tei-c.org/ns/1.0\" quantity=\"10\" type=\"price\">10</measure>",
    "date": "1731",
    "groups": [
      "i",
      ""
    ],
    "path": 1,
    "number_of_pages": 1
  },