Liens entre modèles Escapad et modèles des LMS
==============================================

Cette section est destinée à ceux qui souhaitent comprendre comment sont établies les correspondances entre les modèles de cours parsé depuis le markdown par Escapad et les cours exportés vers les LMS EDX et Moodle. Ces archives EDX ou IMSCC-Moodle sont téléchargeables depuis le site vitrine généré, dans la page de chaque module, section "Réutilisez ce module".

Correspondance entre EDX - Escapad
----------------------------------


La mapping se fait assez naturellement entre le modèle Esc@Pad et le
modèle EDX, même si le typage des activités et contenu ne se fait exactement
au niveau de la sous-section mais sur celui du "component". Voir tableau ci-dessous.

+----------------------------+-------------------------------------------+
| EDX element(:attribute)    | correspondance dans le modèle Esc@pad     |
+============================+===========================================+
| chapter                    | section                                   |
+----------------------------+-------------------------------------------+
| sequential                 | sous-section                              |
+----------------------------+-------------------------------------------+
| sequential:display\_name   | titre de la sous-section                  |
+----------------------------+-------------------------------------------+
| sequential:format          | type de section                          |
+----------------------------+-------------------------------------------+
| sequential:graded (T/F)    | en fonction du type                       |
+----------------------------+-------------------------------------------+
| vertical ("Unité")         | 1 seul "vertical" par sous-section        |
+----------------------------+-------------------------------------------+
| component                  | type de contenu > type de sous-section.   |
+----------------------------+-------------------------------------------+

Les sous-sections Esc@pad peuvent être de 4 types qui sont notées ou pas selon un
type défini dans une "grading policy". Pour Esc@Pad :

-  (ungraded) : cours
-  Compréhension : comprehension
-  Activité : activite
-  Activité Avancé : activite-avancee

Ensuite chaque ``sequential`` peut avoir plusieurs ``vertical`` dénommés
"Unité" dans l'interface, mais dans Esc@pad il n'y a qu'une 'unité' par
sous-section, et l'on se tient à un type de composant par Unité sauf pour les cours avec vidéo qui auront un composant "Html" précédé d'un composant "cn-video" utilisant le plugin spécifique développé pour l'occasion `xblock-cnvideo <https://github.com/CultureNumerique/xblock-cnvideo>`__

Chaque unité peut ensuite contenir différents composant EDX qui seront
déterminé selon le contenu de la sous-section:

+-------------------+--------------------------------------------------+
| composant EDX     | Contenu d'une s-section                          |
+===================+==================================================+
| cnvideo           | video de cours = lien avec ``{: .cours_video}``  |
+-------------------+--------------------------------------------------+
| html              | contenu de cours en HTML                         |
+-------------------+--------------------------------------------------+
| problem           | quiz rédigés en GIFT                             |
+-------------------+--------------------------------------------------+

Stratégie de notation
~~~~~~~~~~~~~~~~~~~~~

Avec EDX il est possible de défninir :

-  Le critère de "passation" du cours, ie la note globale minimale
-  différents types d'exercices notés (ou de notation)
-  pour chaque type:
  -  nombre mini à passer pour être évalué
  -  nombre d'exo que l'on peut sauter
  -  poids dans note globale
  -  nom et nom de code

Tout ceci est défini dans le fichier de template
`templates/toEDX/policies/course/grading_policy.json <../templates/toEDX/policies/course/grading_policy.json>`__

Correspondance des modèles Escapad et Moodle/IMS
------------------------------------------------



Limitations à l'import d'archives IMS dans Moodle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cette procédure d'import vers Moodle au format IMS Common Cartridge a
quelques limitations :

-  un bug affecte la version 3.0 de Moodle et **empêche l'import
   d'archive IMS si les quiz intégré** (au format
   `XMLIMS-QTI <http://www.imsglobal.org/question/qtiv1p2/imsqti_asi_bindv1p2.html#1439623>`__)
   **contiennent au moins une question Vrai/Faux**. `Ce bug a été signalé au groupe de developpement de
   Moodle <https://tracker.moodle.org/browse/MDL-53337>`__; un
   contournement a été inclu dans le code actuel de toIMS.py qui déclare
   les questions Vrai/Faux comme des questions à choix multiples
   (toIMS.py ~l.52).
-  les **paramétrages d'achèvement et de revue des quiz ne sont pas
   conservés**. En effet ces paramètres spécifiques à Moodle ne sont pas
   capturés dans le format IMS. Le comportement limitant vient surtout
   de ce que `les paramètres
   globaux <https://docs.moodle.org/29/en/Common_module_settings>`__,
   qui normalement sont utilisés comme paramètres par défaut lors de la
   création d'un nouveau quiz **ne sont pas pris en compte lors de
   l'import IMSCC**. Ce comportement semble plutôt anormal et `a été
   signalé également <https://tracker.moodle.org/browse/MDL-53422>`__


Correspondance entre les modèles Moodle et Esc@pad
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La correspondance entre les modèles de cours Moodle et le modèle choisi dans Esc@pad sont très proches car
tous les 2 placent le typage des contenus pédagogiques au niveau de la sous-section. Voir ce tableau:

+----------------------------+-------------------------------------------+
| Moodle                     | Esc@pad                                   |
+============================+===========================================+
| Section                    | section                                   |
+----------------------------+-------------------------------------------+
| Activité / Resource        | sous-section                              |
+----------------------------+-------------------------------------------+
| Resource:page              | sous-section: Cours                       |
+----------------------------+-------------------------------------------+
| Activité:quiz              | sous-section:                             |
|                            |                                           |
|                            |    - Compréhension                        |
|                            |    - Activité                             |
|                            |    - ActivitéAvancée                      |
+----------------------------+-------------------------------------------+

Commentaire:

- Le découpage en section est identique
- Les sous-section de Cours sont traduites en Resource Moodel de type "page"
- les 3 types d'activités sont traduits en Activité Moodle de type Quiz.
