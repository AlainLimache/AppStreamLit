import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from graphes_deux_annees import run_comparer_deux_annees
from graphes_une_annee import run_graphes_une_annee
from plot_functions_une_annee import *
from Utils import Utils

def run_home():
    categories_questions = Utils.getCategories_question()
    variables = Utils.getVariables()

    # Configurer le style des graphiques
    sns.set(style="whitegrid", font_scale=1.1, rc={"figure.figsize": (10, 5)})
    plt.rcParams["figure.figsize"] = [10, 5]

   #Utils.add_separator()
    #st.sidebar.title("Navigation")
    #app_mode = st.sidebar.selectbox("Choisissez la page à afficher", ["Page d'accueil", "Une année"])#, "Deux années"])

    #if app_mode == "Page d'accueil":
     #   st.title("Analyse et visualisation de données de qualité de vie au travail")

       # Utils.newLines(2)

        #st.write("""
        #Dans cette application, nous analysons les réponses moyennes en fonction de deux types de variables :
        #1. **Catégorie de question** : Il s'agit de la classification des questions en différentes catégories, comme les questions de CLIMAT SANTE SECURITE, de PRATIQUES CARRIERE, de COMMUNICATION, de JUSTICE, de PARTICIPATION, de CONFIANCE etc.
        #2. **Variable catégorielle** : Il s'agit de variables qui divisent les données en groupes ou en catégories, comme l'âge, le sexe, la profession, le secteur, etc.

        #Les graphiques présentés illustrent la répartition des réponses moyennes en fonction de ces deux types de variables pour chaque année. Ces visualisations permettent de comparer les résultats entre les deux années et d'observer les changements dans la perception de la qualité de vie au travail.
        #""")

    #elif app_mode == "Une année":
    run_graphes_une_annee(categories_questions, variables)

    #lif app_mode == "Deux années":
       # run_comparer_deux_annees(categories_questions, variables)
    
