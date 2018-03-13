.. image:: https://img.shields.io/travis/physumasso/auxiclean.svg?maxAge=600?branch=master
    :target: https://travis-ci.org/physumasso/auxiclean
.. image:: https://img.shields.io/appveyor/ci/fgoudreault/auxiclean/master.svg?maxAge=600
    :target: https://ci.appveyor.com/project/fgoudreault/auxiclean/
.. image:: https://img.shields.io/coveralls/physumasso/auxiclean.svg?maxAge=600?branch=master
    :target: https://coveralls.io/github/physumasso/auxiclean?branch=master
.. image:: https://img.shields.io/badge/licence-MIT-blue.svg
    :target: https://github.com/physumasso/auxiclean/blob/master/LICENCE
.. image:: https://img.shields.io/github/release/physumasso/auxiclean.svg?maxAge=600
    :target: https://github.com/physumasso/auxiclean/releases/latest

Bienvenue sur le projet Auxi-Clean
==================================

Ce projet est une initiative des étudiants et étudiantes au département
de physique de l'Université de Montréal afin de créer une approche
automatisée pour l'attribution des tâches d'assistanat d'enseignement.

Le code source initial a été écrit par Jérémie Tanguay (`Tanjay94 <https://github.com/Tanjay94>`__ sur GitHub).

Compatibilité
-------------

Ce projet fonctionne au moins sur Python version 3.6.
**Ne fonctionne pas pour d'autres versions de Python.**

Installation simple
-------------------

Pour les utilisateurs qui ne sont pas familier avec la programmation et la ligne de
commande, il est possible d'installer et utiliser ce projet sans installer d'interpréteur
Python. Simplement télécharger le fichier compressé sur la page de la `dernière version
disponible <https://github.com/physumasso/auxiclean/releases/latest>`__ sur GitHub.
Il faut télécharger le fichier correspondant à la plateforme souhaitée. Pour MacOS, le fichier à télécharger
est un fichier zip qu'il faut décompresser avant de pouvoir exécuter le .app.
Pour exécuter le programme, il suffit
de cliquer sur le fichier exécutable téléchargé et le tour est joué!

Installation pour Développement
-------------------------------

Pour installer le projet de sorte à avoir accès à l'API, il faut un interpréteur python 3.
Un bon example est `Miniconda <https://conda.io/miniconda.html>`__
produit par Continuum Analytics.

Ensuite, cloner ou télécharger le projet sur le `répertoire officiel 
<https://github.com/physumasso/auxiclean>`__ du projet sur GitHub
et décompresser le fichier si nécéssaire.

Pour installer le module, il faut executer le script d'installation `setup.py`::

  $ python setup.py install

Pour une installation de développement, utiliser l'argument ``develop`` au lieu
de ``install`` car d'autres dépendances sont nécéssaires afin de faire rouler les
tests.

Fonctionnement
--------------

Le code fonctionne en lui donnant un fichiers Excel possédant deux feuilles: une contenant les
données de toutes les candidatures et l'autre contenant les détails sur les
cours à attribuer. Un exemple d'un tel fichier est donné dans le répertoire ``exemples/exemples.xlsx``.
**N.B.: Pour l'instant, le format de ce fichier d'exemple doit absolument être respecté, c'est-à-dire
que les titres des colonnes et les noms des feuilles ne doivent pas changer.**
Une fois ce fichier crée, il suffit d'exécuter le programme (soit en cliquant sur le fichier exécutable
provenant d'une installation simple ou en exécutant le script ``run.py`` pour une
installation de developpement). Exécuter le programme fera apparaître une
interface graphique pour sélectionner le fichier et cliquer sur le bouton **Exécuter**.

**Bien important de fermer le fichier excel avant
d'exécuter le programme, sinon la sélection ne sera pas sauvegardée dans le fichier
excel.**
Alternativement, il est possible d'exécuter la sélection à partir d'un simple script
python:

.. code-block:: python

  from auxiclean import Selector

  chemin = "chemin/vers/le/fichier/excel.xslx"
  Selector(chemin)


L'appel à la classe ``Selector`` fera l'attribution des postes d'auxiliaires d'enseignement
et écrira la sélection dans le même fichier (si le fichier excel n'est pas ouvert), dans une
nouvelle feuille de calcul.


Format du Fichier Excel
***********************

Voici les catégories à remplir pour un cours: 

- Sigle (e.g.: 'PHY3131', 'PHY1441', ...). Si un cours possède plusieurs types de postes
  (des postes avec différentes tâches et nombre d'heures), il faut créer deux cours
  différents dans le fichier excel. Par exemple, 'PHY1441-30' serait le cours désigné
  comme un poste à 30 heures alors que 'PHY1441-90' serait un poste à 90 heures.
  N'importe quelle syntaxe fera l'affaire, en autant que ce soit la même que le sigle
  des cours dans les candidatures (tout doit être consistant).
- Titre du cours.
- Nombre de postes.
- Discipline: la discipline du cours (par exemple pour PHY2710 - Astrophysique et Astronomie,
  la discipline serait 'astrophysique'). Pour des cours sans discipline bien définie,
  il faut spécifier 'générale' ou laisser le champ vide. Si un cours est dans la discipline
  'générale', aucune candidature ne sera favorisée selon le critère de la discipline de
  recherche pour ce cours.
 
Catégories pour la feuilles de candidatures:

- Nom (peut être seulement le matricule ou tout autre chaîne de caractère qui permet
  de différencier les candidatures).
- Maximum: le nombre de postes maximum désiré par la candidature.
- Cycle: le cycle d'étude de la candidature (1, 2 ou 3).
- Cours donnés: la liste de tous les sigles des cours donnés par la candidatures.
  Chaque sigle doit être séparé par une virgule (,). Par exemple, si une candidature aurait
  donné le cours 'PHY1441-30' à deux reprises ainsi que 'PHY3131' à une reprise,
  la case serait remplie de cette façon: 'PHY1441-30, PHY1441-30, PHY3131'.
- Nobels: Le nombre de prix 'petit nobels' gagnés par la candidatures.
- Discipline: à la manière des cours, ceci serait la discipline dans laquelle
  la candidature fait ses recherches. Si aucune discipline particulière ne peut être
  spécifiée, laisser le champ vide ou le remplir avec 'générale'. Si un cours pour
  lequel une candidature de discipline 'générale' applique
  possède une discipline particulière (non 'générale'),
  et pour lequel d'autres candidatures à ce cours sont dans la même discipline. Alors,
  ces autres candidatures seront favorisées par rapport à la candidature 'générale'.
  Par exemple, si une candidature est dans la discipline 'générale' applique pour
  un cours d'astrophysique, alors toute autre candidature dont la discipline est
  l'astrophysique sera favorisée par rapport à la première candidature selon ce critère.
- Cote Z: la cote Z de la candidature.
- Choix: La liste des cours désirés par une candidature selon la même syntaxe que la
  catégorie des 'Cours donnés'.

Dans tous les cas, les titres des colonnes des feuilles du fichier excel ne doivent
pas changer du même que les titres des feuilles.

Contribution
------------

Pour contribuer au projet, simplement faire un fork du projet sur GitHub
et soumettre des pull requests ou bien contacter un des responsable
du projet via la `PHYSUM <http://www.aephysum.umontreal.ca/>`__.

Pour les développeurs, il y a des unittests qui sont écrits afin d'aider
le développement et pour vérifier que tout marche encore. Ces tests
sont exécutés par le CI runner Travis pour tous les Pull Requests.
Pour les exécuter sur une machine locale, s'assurer d'avoir
installer le module en mode 'develop'::
  
  $ python setup.py develop

Et pour exécuter les tests, il suffit de lancer `pytest` (requiert d'avoir installé `pytest-cov` ce qui est
fait automatiquement via le script d'installation)::

  $ pytest

Pour recréer les fichiers exécutables comme sur la page des `releases <https://github.com/physumasso/auxiclean/releases/latest>`__ sur GitHub,
il faut installer **pyinstaller**::

  $ pip install pyinstaller

et exécuter la commande::
 
  $ pyinstaller --onefile --windowed --clean --name=auxiclean_executable run.py

Cette commande compilera le fichier `run.py` sous une forme exécutable dépendamment de
la plateforme utilisée. Attention, pyinstaller ne fonctionne pas en python 3.6. Il faut donc exécuter
cette commande soit sous une version de python 3.5 ou inférieure ou soit dans un environnement
virtuel.

POUR LES ADMINS: lorsqu'un PR est fait, les tests sont roulés à la fois sur Windows (Appveyor) que
sur MacOS et linux (travis). Le code coverage est rapporté avec coveralls, ceci permet de toujours s'assurer
que le code fonctionne après chaque modification. Il est donc important d'écrire des tests en conséquence si
l'API change. De plus, les fichiers exécutables pour chaque release sont compilés et uploadés automatiquement
sur GitHub. Ainsi, dès qu'une nouvelle release est crée, Appveyor s'occupera de créer le fichier exécutable
pour Windows et travis pour MacOS et Linux, pas besoin de les créer manuellement (voir les fichiers
`.travis.yml <https://github.com/physumasso/auxiclean/blob/master/.travis.yml>`__ et
`.appveyor.yml <https://github.com/physumasso/auxiclean/blob/master/.appveyor.yml>`__ )

Contributeurs
-------------

La liste de tous les contributeurs au code:

- Jérémie Tanguay (`Tanjay94 <https://github.com/Tanjay94>`__)
- Félix Antoine Goudreault (`fgoudreault <https://github.com/fgoudreault>`__)
