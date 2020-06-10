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

