﻿.. image:: https://img.shields.io/travis/physumasso/auxiclean.svg?maxAge=600?branch=master
    :target: https://travis-ci.org/physumasso/auxiclean
.. image:: https://img.shields.io/appveyor/ci/fgoudreault/auxiclean/master.svg?maxAge=600
    :target: https://ci.appveyor.com/project/fgoudreault/auxiclean/
.. image:: https://img.shields.io/coveralls/physumasso/auxiclean.svg?maxAge=600?branch=master
    :target: https://coveralls.io/github/physumasso/auxiclean?branch=master
.. image:: https://img.shields.io/badge/licence-MIT-blue.svg
    :target: https://github.com/physumasso/auxiclean/blob/master/LICENCE
.. image:: https://img.shields.io/github/release/physumasso/auxiclean.svg?maxAge=600
    :target: https://github.com/physumasso/auxiclean/releases

Bienvenue sur le projet Auxi-Clean
==================================

Ce projet est une initiative des étudiants et étudiantes au département
de physique de l'Université de Montréal afin de créer une approche
automatisée pour l'attribution des tâches d'assistanat d'enseignement.

Le code source initial a été écrit par Jérémie Tanguay (`Tanjay94 <https://github.com/Tanjay94>`__ sur GitHub).


Installation
------------

Pour installer le projet, il faut un interpréteur python 3.
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
Une fois ce fichier créer, il suffit d'appeler la classe ``Selector`` de cette façon

.. code-block:: python

  from auxiclean import Selector
  
  chemin = "chemin/vers/le/fichier/excel.xslx"
  s = Selector(chemin)
  
L'appel à cette classe fera l'attribution des postes d'auxiliaires et l'écrira dans le même
fichier Excel qu'au départ, dans une nouvelle feuille.

Contribution
------------

Pour contribuer au projet, simplement faire un fork du projet sur GitHub
et soumettre des pull request ou bien contacter un des responsable
du projet via la `PHYSUM <http://www.aephysum.umontreal.ca/>`__.

Pour les développeurs, il y a des unittests qui sont écrits afin d'aider
le développement et pour vérifier que tout marche encore. Ces tests
sont exécutés par le CI runner Travis pour tous les Pull Requests.
Pour les exécuter sur une machine locale, s'assurer d'avoir
installer le module en mode 'develop'::
  
  $ python setup.py develop

Et pour exécuter les tests, il suffit d'exécuter le script `tests.py`::

  $ python tests.py

Contributeurs
-------------

La liste de tous les contributeurs au code:

- Jérémie Tanguay (`Tanjay94 <https://github.com/Tanjay94>`__)
- Félix Antoine Goudreault (`fgoudreault <https://github.com/fgoudreault>`__)
