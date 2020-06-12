# Algorithm

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

## Errors in date extraction
- 1734-55 > 1734
- CAT_000086_e196:  [L. a. s.; 1825; 1 p. in-4. 2] > ø [fixed]
- CAT_000086_e171: né à Rodez en 1767 [-J.-H. de), poète distingué, né à Rodez en 1767. -1° L. a. s. à M. Déhault, 10 flor, an XII, 3 p. in-4. Légère déchirure toute relative à sa traduction de l'Enéide. -2° Sa biographie, pièce aut. de M. Villenave, 11 p. in-4. 5]
- CAT_000123_e148: Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798 [Pièce de vers aut. sig. sig. aussi par sa femme Caroline Vanhove: 18 janvier 1798, 1 p. in-8 obl. 22]
- CAT_000123_e81: L. a. s. au comte de Villèle : 14 avril 1826 [L. a. s. au comte de Villèle : 14 avril 1826, 1 p. in-fol. 15] [fixed]
- CAT_000123_e81: au comte de Villèle : 14 avril 1826 [L. a. s. au comte de Villèle : 14 avril 1826, 1 p. in-fol. 15] [fixed]
- CAT_000102_e135: Leipzig. « juin 1846 [Morceau de musique aut. sig.; Leipzig. « juin 1846, 1/2 p. in-8 obl. 15]


