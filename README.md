# Magicplot for CEM

Magicplot for CEM est une interface graphique en Python utilisant le Framework PyQt5.

![Interface de magicplot](Doc/images/magicplot.jpeg "Interface de magicplot")

Le but de ce programme est de pouvoir traiter rapidement et facilement les mesures faites à l'aide de l'analyseur de spectre.

## Avancement du projet

### Opérationel

- Interface opérationelle
- Ouverture de 1 ou plusieurs fichiers
- Plot de 1 ou plusieurs courbes
- Crosshair et coordonnées fonctionnels
- Plot le max de X courbes (Comparaison de valeur pour chaque fréquence donnée)
- Sauvegarde dans un fichier CSV de ces valeurs max
- Renomage des fichiers en .csv (Pour les fichiers venant de l'analyseur)
- Traitement du CSV (Suppressions des informations inutiles, ajout de header)


### En cours de dev

#### Important pour RC
- Plaçage d'un marqueur via le curseur de la souris (clique aux coordonées)

#### Bonus
- Ajout de configuration référence (Courbe de référence pour chaque modèle de robot)
- Permettre de connaitre l'angle à laquelle a été prise une mesure
- Plot un graphique en 3D (Fréquence, Niveau, Angle) pour le max
