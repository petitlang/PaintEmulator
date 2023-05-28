Chef de projet :       HUYNH Huu Thanh Tu                Projet d'informatique : Paint Application
Membre d'équipe : LI Mouzheng	 		ASINSA  Group 96,  INSA Lyon
                              YE Chengzhi


		PAINT APPLICATION BY PYTHON

-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

I/   Contenu du dossier
----> Classes :
       1/ gui.py                       IHM de l'application, LANCER cette .py pour démarrer l'application "Paint Emulator"
	 2/ image_widget.py		   Classes définit des widgets concernant l'image où l'utilisateur va dessiner/modifier
	 3/ menu.py				   Classe definit le menu de l'application
	 4/ panel.py			   Modèle d'interface commun pour des différents panneaux
	 5/ Draw.py				   Classe définit des outils de dessiner
	 6/ select_zone.py		   Classe définit la fonction spécifique pour selectionner une zone sur l'image
	 7/ txt_recogn.py			   Module permet la détection et la reconnaissance de texte dans une image

----> Images et arrière-plan : 
	 Les images que l'on a mis dans le dossier "img" servent à définir l'icone et l'arrière plan

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

II/  Installation
----> Installez le module customtkinter avec pip :   
	pip3 installer customtkinter
( Ou mettre à jour l'installation existante : pip3 install customtkinter --upgrade )
----> Installez le module Pillow avec pip : 
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade Pillow
----> Installez les modules necessaires pour exécuter le fichier ---> Ouvrir le fichier Text Recognition Script - README.md pour plus informations.

-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

III/ Utilisation
----> Après décompression de l'archive zip et l'installation des librairies nécessaires, exécutez le fichier gui.py pour lancer l'application ;
----> Nous proposons quasiment toutes les fonctionnalités de "Microsoft Paint", comme la dessine optimisée, les opérations sur l'image, la sélection d'une partie d'image et la couper ou la copier pour la coller ailleurs ;
----> L'utilisateur peut importer leur images désirées pour les traiter dans notre programmes, et nous présentons plusieurs formats pour sauvegarder les images modifiés ;
----> Nous ajoutons encore une analyse de chaîne de caractère composée de lettres et de numéros, et d'autres surprises à vous de les découvrir ...

-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

Bonne créativité pour vous tous les artistes ! Meow ~~~ <3