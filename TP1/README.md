# TP 1
## Présentation de l'ordinateur sur lequel le TP a été effectué

L'ordinateur sur lequel le TP a été réalisé est un intel celeron possédant 8 coeurs physiques de calcul sous Linux. Voici la sortie 
que nous a donné lscpu :

```verbatim
Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         39 bits physical, 48 bits virtual
  Byte Order:            Little Endian
CPU(s):                  8
  On-line CPU(s) list:   0-7
Vendor ID:               GenuineIntel
  Model name:            Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz
    CPU family:          6
    Model:               158
    Thread(s) per core:  2
    Core(s) per socket:  4
    Socket(s):           1
    ...
Caches (sum of all):                        
Caches (sum of all):     
  L1d:                   128 KiB (4 instances)
  L1i:                   128 KiB (4 instances)
  L2:                    1 MiB (4 instances)
  L3:                    6 MiB (1 instance)
```

## Produit matrice-matrice

### Tests sur la permutation des boucles

Dans un premier temps, on s'est contenté de permuter les boucles pour le produit matrice-vecteur et nous avons regarder pour diverses
dimensions le temps pris pour calculer le produit matrice-matrice. Voici les résultats obtenus dans le tableau suivant (en MFlops (secondes)) :


| Ordre des boucles | dim 1023 | dim 1024 | dim 1025 |
|-------------------|----------|----------|----------|
|        ijk        |     1.32s; 1614.25 MFlops     |     3.67s; 619.54 MFlops     |     1.35s; 1590.2 MFlops     |
|        ikj        |     9.33s; 229.28 MFlops     |     11.98s; 179.19 MFlops     |     9.94s; 216.62 MFlops     |
|        jik        |     2.25s; 950.35 MFlops     |     4.50s; 477.16 MFlops     |     2.26s; 950.35 MFlops     |
|        jki        |     1.02s; 2039.26 MFlops     |     1.03s; 2074.42 MFlops     |     1.05s; 2048.88 MFlops     |
|        kij        |     9.11s; 234.99 MFlops     |     10.07s; 213.18 MFlops     |     9.76s; 220.49 MFlops     |
|        kji        |     0.91s; 2345.03 MFlops     |     0.84s; 2539.05 MFlops     |      0.86s; 2502.34 MFlops     |

#### Observation

Il est clair que les meilleures performances sont obtenues lorsque la boucle en $i$ est la plus interne.
De plus, dans ce cas, la variation du temps de calcul en fonction de la dimension de la matrice devient insignifiante. Les meilleures
performances étant obtenues avec les boucles dans l'ordre $kji$. 

### Interprétation

On sait que la matrice est stockée par colonne, et donc que le premier indice est celui qui en variant permet 
d'accéder à des données contigües en mémoire. Puisque le produit matrice vecteur fait apparaître dans la boucle la plus interne le calcul 
$C_{ij} \leftarrow C_{ij} + A_{ik}.B_{kj}$, on voit qu'en mettant la boucle en $i$ comme la plus interne, cela permet d'accéder aux 
coefficients de $C$ et de $A$ en contigü dans la mémoire, tandis que pour $B$, on conserve la même valeur durant toute la boucle interne. 

En revanche, lorsque la boucle en $j$ est la plus interne, on obtient les plus mauvais performances puisque dans ce cas, l'accès aux 
coefficients de $C$ et de $B$ se fait avec des sauts mémoires dont la distance est égale à la dimension de la matrice. De plus, si la 
taille de la matrice est une puissance de deux, on tombera plus souvent sur une adresse mémoire de la mémoire cache qui contient déjà une valeur
lue ou écrite récemment, ce qui explique cette sensibilité à la dimension de la matrice (ce qui n'est pas le cas lorsque la boucle en $i$ 
est la plus interne, puisque dans ce cas on lit les coefficients en contigü).

### Conclusions

On voit qu'il est important de comprendre comment marche la mémoire cache afin d'obtenir une bonne optimisation de nos codes.
Dans le cas du produit matrice-matrice, on voit que les gains obtenus sont très significatifs et nous invite à devoir réfléchir dans les 
sections critiques en temps de nos codes à réfléchir sur la façon dont on accèdera aux données (et à la représentation des donnée en mémoire).
