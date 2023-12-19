# Configuration et dépendances:  
    1) Créer un environnement virtuel (seulement au premier lancement, sinon passer à l'étape 2):  
        Utiliser Python ou Python3, selon votre installation:  
            python3 -m venv venv  
            ou  
            python -m venv venv  
  
    2) Activer l'environnement virtuel:  
        Sous Linux / MacOS:  
            source venv/bin/activate  
        Sous Windows:  
            # Avec cmd.exe:  
                venv\Scripts\activate.bat  
            # Avec PowerShell:  
                venv\Scripts\Activate.ps1  
  
    3) Installer les dépendances (seulement au premier lancement de l'environnement virtuel, sinon passer à l'étape 4):  
        pip install -r requirements.txt  
        pip install matplotlib  
        pip install streamlit  
        pip install scikit-learn  
        pip install seaborn  
        pip install plotly  
  
    4) Lancer l'application Streamlit en local:  
        streamlit run app.py  
  
  
# Structure du projet :
  Racine du projet :
    - graphes_deux_annees.py : contient les fonctions de traçage des graphes pour deux années 
    - graphes_une_annees.py : contient les fonctions de traçage des graphes pour une année
    - home.py : contient les fonctions d'affichage de la page d'accueil
    - plot_functions_deux_annees : contient les fonctions de création des graphes pour deux années
    - plot_functions_une_annee : contient les fonctions de création des graphes pour une année
    - app.py : fichier principal de l'application  
    - Utils.py : contient des fonctions utilitaires utilisées par les autres fichiers .py  

  Dossier data :
    - Data1007.csv : données fournies au début du projet (non_modifiées)
    - Data1007.xlsx : même chose que Data1007.csv mais sous un format différent
    - New_Data1007.csv : nouveau jeu de données généré
    - generation.py : contient les fonctions de génération du nouveau jeu de données
  
  
# Utilisation de l'application :  
    1) Importer le fichier Data1007.csv (pour une année) et, si besoin, le fichier New_Data1007.csv (pour deux années) situé dans le dossier "data"  
    2) Choisir les variables à afficher dans l'application grâce aux options à gauche de la page
    3) Survoler avec la souris les différents graphes pour obtenir des informations plus précises (valeur exacte, catégorie correspondante, etc)
    4) Si besoin, des options d'affichage (zoom, plein écran) sont disponibles en haut à droite de chaque graphe

# Génération d'un nouveau fichier CSV :  
    Exécuter le script generation.py  
    Ceci générera un nouveau fichier nommé NewData1007.csv contenant des données modifiées.  
    Note: - Seules les données relatives aux moyennes seront modifiées, les réponses aux questions resteront inchangées.
        - Le séparateur pour le fichier CSV est ";"   
  
  