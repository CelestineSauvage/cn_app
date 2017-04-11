Contribuer au code d'Esc@pad
============================

Cette section est dédiée aux contributeurs du code d'Escapad et décrit les besoins prioritaires déjà identifiés.
Au 15 décembre 2016, Esc@pad a atteint son premier objectif: faire la preuve du concept d'une chaine éditoriale intégrée permettant de créer à partir d'un fichier source en format texte un contenu pédagogique riche disponible en plusieurs formats (Web, EDX, Moodle). Les besoins prioritaires se décomposent pour l'instant en 3 grands catégories (détaillés ci-après à la suite de l'architecture globale du code)


Architecture
------------

Le code d'Escapad est décomposé comme suit:

- le parser dont le point d'entrée est ``src/cnExport.py``
- l'application Web qui exécute le script du parser via une application Django
- le fichier "requirements.txt" contient les dépendances pour ces 2 parties du code.

**Le parser**

Cette partie du code réside dans les dossiers:

- src:
    - cnExport.py : c'est le script de départ; il amorce le parsing et contrôle les différents exports directement (Web) ou via  toEDX.py ou toIMS.py.
    - model.py : contient le modèle; le parsing est amorcé par la création d'un objet Module défini dans ce modèle
    - fromGIF.py : responsable du découpage et du parsing des questions rédigées en GIFT dans les sous-section de type Activité; gère également l'export web des questions
    - utils.py : contient quelques méthodes utilitaires pour l'écriture de fichiers et certains filtres
- templates: La génération du mini-site et de l'archive EDX utilise des templates écrit en Jinja2 et situé dans ce dossier. Pour le mini-site web
- static : dossier regroupant les fichiers js, css, etc. utilisés par la version mini-site web de l'export. Ce dossier est donc copié tel quel dans chaque export web.
- logs : contient les logs uniquement pour cnExport

**l'application web**

Cette application web est écrite au sein du framework Django (version 10). Tout le code écrit suit la documentation au plus près. Il est conseillé de faire au moins le premier tutoriel Django pour prendre en main ce framework.

Son code est situé dans les dossiers:

- cn_app : paramètres globaux
- escapad : la "sous-application" qui gère les dépôts:

    - admin.py : paramétrage de l'interface d'admin utilisée et localisée à l'url `/admin`. C'est la seule interface web permettant d'interagir avec l'application Escapad.
    - apps.py : paramétrage de l'application
    - forms.py : utilisé par l'interface d'admin pour effectuer certaines opérations avant la soumission d'un nouvel objet Repository
    - models.py : défini le modèle de Repository
    - signals.py : exploite le mécanisme de signals de Django et relié donc au évènements de création, édition, ou suppression d'objets Repository
    - urls.py : définition des patterns d'urls spécifique à l'application escapad
    - views.py : définition du code permettant de faire exécuter le script pour un dépôt donné. L'emplacement des fichiers sources et les fichiers générés est défini dans le fichier site_settings.py et expliqué dans la documentation d'installation
    - utils.py : qqs méthodes utilitaires, notamment celle à qui est délégué l'exécution du script cnExport.py
- les logs de l'application Django sont situés dans le fichier debug.log dont l'emplacement est défini dans le fichier cn_app/site_settings.py
- le fichier manage.py n'est pas à modifier à priori (sauf cas avancé)


Couverture de tests
--------------------

La stratégie de tests présente différents aspects:

1. le test du parsing des fichiers de code source de cours qui aboutit à la construction d'un modèle de cours (cf :class:`model.Module`); dans ce cas on compare les objets générés avec un objet de contrôl sérialisé (`tests.config.json`)
2. le test de la génération des exports Web (cf :mod:`cnExport`), IMS-CC (:mod:`toIMS`), et EDX (:mod:`toEDX`); ici ce seront les archives générés qui seront comparés avec des archives de contrôle.
3. le test des web services développés en Django: dans ce cas il s'agit de contrôler la manipulation des fichiers et l'exécution des appels web.
4. enfin, une stratégie de test plus granulaire qui consiste à tester chaque méthode séparemment en vérifiant la cohérence des entrées et sorties (WIP).

Pour lancer les tests:

- ``$ cd tests``
- ``$ python tests.py``


Tests globaux controllant le résultat
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ce type de test est développé dans le module :mod:`tests`:

- les tests écrits utilisent le framework de test Python `UnitTest <https://docs.python.org/2/library/unittest.html>`_
- le fichier ``module_test.md`` est le fichier source de test
- le fichier ``tests.config.json`` est chargé comme objet de contrôle

Le test :class:`tests.ModuleParsingTestCase` récupère d'un côté l'objet sérialisé de contrôle, de l'autre parse le fichier de test pour produire un objet `Module` de test (cf :func:`tests.setUp`). La correspondance entre les champs est ensuite comparée dans la fonction :func:`tests.runTest`, en prenant soin de comparer de manière progressive, en comparant d'abord simplement le nombre de sections, puis en comparant l'exact identité de l'objet de test et de l'objet de contrôle.

Ajouter des tests
~~~~~~~~~~~~~~~~~

Le test :class:`tests.HtmlGenerationTestCase` (en cours) vise quant à lui à comparer un export web de contrôle avec un export web généré à partir du fichier source de test. Pour développer un nouveau test, il est possible de définir des sous-classes de :class:`tests.ModuleParsingTestCase`, ce qui permet de réutiliser le mécanisme de lancement du test (setUp).

Tests unitaires au niveau des méthodes du parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un autre type de test doit être développé pour permettre de vérifier le bon fonctionnement du parsing à partir de la formalisation du bon déroulement de chaque étape du parsing au niveau des méthodes des classes définies dans ``src/model.py``.



Documentation des tests
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: tests
    :members:





Amélioration du parser
----------------------

Il s'agit ici de consolider le code de la partie parser (cf dossier `src`) selon différents aspects:
- intégrer la librairie [pygiftparser](https://github.com/mtommasi/pygiftparser) afin de remplacer `fromGIFT.py` pour le parsing du GIFT.
- étendre la librairie [pygiftparser](https://github.com/mtommasi/pygiftparser) pour augmenter la couverture de la spécification GIFT (aujourd'hui partielle)
- proposer une version du script `cnExport.py` pour produire un site mono-module sans page d'accueil
- homégénéiser et factoriser le code de génération des archives:
  - passer la génération de l'IMS-CC via un template Jinja2 (comme pour le web et EDX)
  - coder en objet ces "Exporters" qui peuvent se décliner en IMSExporter, WebExporter, etc.


Améliorer application Web (sous Django)
---------------------------------------

Enrichir les fonctionalités, en particulier du côté de l'application web en Django (contenue dans les sous-dossiers `cn_app` et `escapad`):

- proposer une version sans persistence et sans Git et prenant directement un seul fichier markdown:
    - un formulaire prenant un fichier markdown en entrée, plus qqs champs calqués sur les options de `src/cnExport.py` (le script exécuté)
    - validation
    - création d'un dossier temporaire et upload du fichier à l'intérieur
    - génération du site en mode mono-module sans page d'accueil
    - compression en zip du dossier compilé
    - renvoi à l'usager du zip
    - effacement du dossier temporaire
- passer en web service la version ci-avant
- développer une interface HTML5 permettant d'écrire du markdown+ gift avec panel de rendu reprenant l'export web des modules (épuré ?)
- coloration syntaxique du GIFT
- etc. etc. :)
