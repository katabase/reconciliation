import unittest

from extractor import *


class Nb_pages(unittest.TestCase):
    maxDiff = None
    def test_nb_pages(self):
        liste_test = [
            ['L. a. s., 1 p. 1/2 in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3',
                'CAT_000139_e390_1', 'Belair', 'Avril 1891'],
            ['L. a. s., t. p. in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3',
                'CAT_000139_e390_2', 'Belair', 'Avril 1891'],
            ['L. a. s., I p.  1/2 in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3',
                'CAT_000139_e390_3', 'Belair', 'Avril 1891']
            ]

        test_dict_entree = {
            "CAT_000139_e390_1": {
                "desc": "L. a. s., 1 p. in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3",
                "price": 3,
                "date": None,
                "author": "Belair",
                "sell_date": "Avril 1891"
            },
            "CAT_000139_e390_2": {
                "desc": "L. a. s., t p. in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3",
                "price": 3,
                "date": None,
                "author": "Belair",
                "sell_date": "Avril 1891"
            },
            "CAT_000139_e390_3": {
                "desc": "L. a. s., I p.  1/2 in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3",
                "price": 3,
                "date": None,
                "author": "Belair",
                "sell_date": "Avril 1891"
            }
        }
        actual = pn_extractor(liste_test, test_dict_entree)
        test_dict_sortie = {
            "CAT_000139_e390_1": {
                "desc": "L. a. s., 1 p. in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3",
                "price": 3,
                "date": None,
                "number_of_pages": 1.5,
                "author": "Belair",
                "sell_date": "Avril 1891"
            },
            "CAT_000139_e390_2": {
                "desc": "L. a. s., t p. in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3",
                "price": 3,
                "date": None,
                "number_of_pages": None,
                "author": "Belair",
                "sell_date": "Avril 1891"
            },
             "CAT_000139_e390_3": {
                "desc": "L. a. s., I p.  1/2 in-8. Curieux papier à soit chiffre où se trouve grave un canard avec le mot couac. 3",
                "price": 3,
                "date": None,
                "number_of_pages": 1.5,
                "author": "Belair",
                "sell_date": "Avril 1891"
            }
        }
        self.assertDictEqual(actual, test_dict_sortie)

if __name__ == '__main__':
    unittest.main()
