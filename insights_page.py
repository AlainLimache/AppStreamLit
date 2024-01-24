import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from plot_functions_une_annee import *
from insights_plot import *
from insigths_calculations import *
from Utils import Utils

def run_page_insights(authenticator, role, qualifiers, variables):
    # Configurer le style des graphiques
    sns.set(style="whitegrid", font_scale=1.1, rc={"figure.figsize": (10, 5)})
    plt.rcParams["figure.figsize"] = [10, 5]

    
    variables = list()
    qualifiers = list()
    radio_buttons = dict()

    insights_strong = list()
    insights_medium = list()
    insights_weak = list()
    insights_none = list()

    if "nbInsightsToShow" not in st.session_state:
        print("COUCOU 1")
        st.session_state.nbInsightsToShow = 10
        print(st.session_state.nbInsightsToShow)

    st.title("Analyse et visualisation de données de qualité de vie au travail pour une année")

    Utils.newLines(2)

    st.write("""
    Dans cette application, nous analysons les réponses moyennes en fonction de deux types de variables :
    1. **Catégorie de question** : Il s'agit de la classification des questions en différentes catégories, comme les questions de CLIMAT SANTE SECURITE, de PRATIQUES CARRIERE, de COMMUNICATION, de JUSTICE, de PARTICIPATION, de CONFIANCE etc.
    2. **Variable catégorielle** : Il s'agit de variables qui divisent les données en groupes ou en catégories, comme l'âge, le sexe, la profession, le secteur, etc.

    Les graphiques présentés illustrent la répartition des réponses moyennes en fonction de ces deux types de variables pour chaque année. Ces visualisations permettent de comparer les résultats entre les deux années et d'observer les changements dans la perception de la qualité de vie au travail.
    """)

    Utils.newLines(2)

    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

    st.sidebar.title("Filtres")
    strong_toggle = st.sidebar.checkbox("Afficher les insights forts", value=True)
    medium_toggle = st.sidebar.checkbox("Afficher les insights moyens", value=False)
    weak_toggle = st.sidebar.checkbox("Afficher les insights faibles", value=False)
    none_toggle = st.sidebar.checkbox("Afficher les insights nuls", value=False)

    st.sidebar.title("Type de graphique")
    graph_type = st.sidebar.radio("Type de graphique :", options=["Barres", "Graph", "Boites"], index=0, horizontal=True)

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, delimiter=';', index_col=0)
        
        st.sidebar.title("Types de variables")
        for column in data.columns:
            index = 1
            if data[column].dtype == 'object':
                index = 0
            radio_buttons[column] = st.sidebar.radio(column + ":", options=["Descriptive", "Réponce", "Ignorer"], index=index, horizontal=True)
            if radio_buttons[column] == "Descriptive":
                variables.append(column)
                if column in qualifiers:
                    qualifiers.remove(column)
            elif radio_buttons[column] == "Réponce":
                qualifiers.append(column)
                if column in variables:
                    variables.remove(column)
            elif radio_buttons[column] == "Ignorer":
                if column in qualifiers:
                    qualifiers.remove(column)
                if column in variables:
                    variables.remove(column)

        # Nouvelle colonne pour la réponse moyenne calculée
        data['REPONSE_MOYENNE'] = data[qualifiers].sum(axis=1) / len(qualifiers)

        Utils.newLines(3)
        st.write("### Données")
        st.write(data)
        Utils.newLines(1)

        # Formater les noms des gatégories
        #formatted_categories = [Utils.format_awnser_name(awnser) for awnser in qualifiers]
        #awnser_mapping = dict(zip(formatted_categories, qualifiers))

        Utils.add_separator()

        #-----------------------------------------------------------------------

        st.header("Visualisations")
        Utils.newLines(1)
        if not strong_toggle and not medium_toggle and not weak_toggle and not none_toggle:
            st.write("Aucun type d'insight n'a été sélectionné. Veuillez sélectionner au moins un type d'insight dans le menu de gauche.")

        #-----------------------------------------------------------------------


        for variable in variables:            
            for awnser in qualifiers:
                if data[variable].nunique() <= 2:
                    # CHI2 si moins de 2 valeurs uniques ?
                    pvalue = cochran_armitage_test(data[[variable, awnser]], variable, awnser)
                else:
                    pvalue = kruskal_test(data[[variable, awnser]], variable, awnser)
                combo = {
                    "variable": variable,
                    "awnser": awnser,
                    "pvalue": pvalue
                }

                #insights_strong.append(combo)
                if pvalue < 0.05:
                    insights_strong.append(combo)
                elif pvalue < 0.1:
                    insights_medium.append(combo)
                elif pvalue < 0.2:
                    insights_weak.append(combo)
                else:
                    insights_none.append(combo)
                
                
            
        
        insights_strong = sorted(insights_strong, key=lambda x: x["pvalue"])
        insights_medium = sorted(insights_medium, key=lambda x: x["pvalue"])
        insights_weak = sorted(insights_weak, key=lambda x: x["pvalue"])
        insights_none = sorted(insights_none, key=lambda x: x["pvalue"])

        insights_to_show = list()

        if strong_toggle:
            insights_to_show += insights_strong
        
        if medium_toggle:
            insights_to_show += insights_medium
        
        if weak_toggle:
            insights_to_show += insights_weak
        
        if none_toggle:
            insights_to_show += insights_none
            
        
        if len(insights_to_show) == 0:
            st.write("Aucun insight séléctionné n'a été trouvé.")
        else:
            for insight in insights_to_show[:st.session_state.nbInsightsToShow]:
                display_data(data, insight, graph_type)
            if len(insights_to_show) > st.session_state.nbInsightsToShow:
                st.write("Il y a encore ", len(insights_to_show) - st.session_state.nbInsightsToShow, "insights à afficher.")
                Utils.newLines(1)
                show_more_button = st.button("Afficher plus")
                if show_more_button:
                    st.session_state.nbInsightsToShow += 10
        
        st.write("Dedans : " + str(st.session_state.nbInsightsToShow))


        #-----------------------------------------------------------------------

    else:
        st.warning("Veuillez importer un fichier CSV.")






