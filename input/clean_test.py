import unittest
from clean_xml import desc_correction

test_desc_1="P a s et Pa à Pascal, à Morel,2 p 1 / 2 in4° obl, cachet. 10"
test_result_1="P. a. s. et P. a. à Pascal, à Morel, 2 p. 1/2 in-4 obl., cachet. 10"
test_desc_2="L aut sig; 3 p 3/ 4 inf°."
test_result_2="L. aut. sig.; 3 p. 3/4 in-f."
test_desc_3="D.a s   et  L aut sig, in12 et in-4° ( de 2 p pl 3 /4 )"
test_result_3="D. a. s. et L. aut. sig., in-12 et in-4 (de 2 p. pl. 3/4)"
test_desc_4="P a, Michel de l'Acad fr in18°, 3 p, 10"
test_result_4="P. a., Michel de l'Acad. fr. in-18, 3 p., 10"
test_desc_5="Las à Lasserre"
test_result_5="L. a. s. à Lasserre"
test_desc_6="La sig infol° obl; 4 p pl, à Damien.. . ., 11 50"
test_result_6="L. a. sig. in-fol. obl.; 4 p. pl., à Damien…, 11.50"


class TestCarre(unittest.TestCase):
    #Test each assertion previously defined

    def test_calcul_correct(self):
        self.assertEqual(desc_correction(test_desc_1), test_result_1)
        self.assertEqual(desc_correction(test_desc_2), test_result_2)
        self.assertEqual(desc_correction(test_desc_3), test_result_3)
        self.assertEqual(desc_correction(test_desc_4), test_result_4)

if __name__ == '__main__':
    unittest.main()
