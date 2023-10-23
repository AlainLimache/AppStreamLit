import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from plot_functions_deux_annees import *
from Utils import Utils

def run_comparer_deux_annees(authenticator, role, categories_questions, variables):
    # Configurer le style des graphiques
    sns.set(style="whitegrid", font_scale=1.1, rc={"figure.figsize": (10, 5)})
    plt.rcParams["figure.figsize"] = [10, 5]

    st.title("Comparaison, analyse et visualisation de données de qualité de vie au travail pour deux années")

    Utils.newLines(2)

    st.write("""
    Dans cette application, nous analysons les réponses moyennes en fonction de deux types de variables :
    1. **Catégorie de question** : Il s'agit de la classification des questions en différentes catégories, comme les questions de CLIMAT SANTE SECURITE, de PRATIQUES CARRIERE, de COMMUNICATION, de JUSTICE, de PARTICIPATION, de CONFIANCE etc.
    2. **Variable catégorielle** : Il s'agit de variables qui divisent les données en groupes ou en catégories, comme l'âge, le sexe, la profession, le secteur, etc.

    Les graphiques présentés illustrent la répartition des réponses moyennes en fonction de ces deux types de variables pour chaque année. Ces visualisations permettent de comparer les résultats entre les deux années et d'observer les changements dans la perception de la qualité de vie au travail.
    """)
            
    Utils.newLines(2)

    uploaded_file1 = st.file_uploader("Choisissez un fichier CSV pour l'année 1", type="csv")
    uploaded_file2 = st.file_uploader("Choisissez un fichier CSV pour l'année 2", type="csv")

    if ((uploaded_file1 is not None) and (uploaded_file2 is not None)):
        data1 = pd.read_csv(uploaded_file1, delimiter=';', index_col=0)
        data2 = pd.read_csv(uploaded_file2, delimiter=';', index_col=0)

        # Nouvelle colonne pour la réponse moyenne calculée
        data1['REPONSE_MOYENNE'] = data1[categories_questions].sum(axis=1) / len(categories_questions)
        data2['REPONSE_MOYENNE'] = data2[categories_questions].sum(axis=1) / len(categories_questions)

        # Ajoutez une colonne d'année aux données
        data1['YEAR'] = 'Année 1'
        data2['YEAR'] = 'Année 2'

        # Concaténez les deux jeux de données
        combined_data = pd.concat([data1, data2], ignore_index=True)

        Utils.newLines(3)
        st.write("### Données pour l'année 1")
        st.write(data1)

        Utils.newLines(1)
        st.write("### Données pour l'année 2")
        st.write(data2)

        Utils.newLines(1)

        # Formater les noms des gatégories
        formatted_categories = [Utils.format_category_name(category) for category in categories_questions]
        category_mapping = dict(zip(formatted_categories, categories_questions))

        Utils.add_separator()
        st.sidebar.title("Options")

        #-----------------------------------------------------------------------

        st.sidebar.subheader("Graphe 1")
        var1_1 = st.sidebar.selectbox("Choisissez une variable catégorielle pour le premier graphe",
                                                options=variables,
                                                index=0)
        Utils.add_separator()

        st.sidebar.subheader("Graphe 2")
        var2_1 = st.sidebar.selectbox("Choisissez une variable catégorielle pour le deuxième graphe",
                                                options=variables,
                                                index=0)
        var2_2 = st.sidebar.selectbox("Choisissez une deuxième variable catégorielle pour le deuxième graphe",
                                                options=variables,
                                                index=9)
        
        Utils.add_separator()

        st.sidebar.subheader("Graphes 3 et 4")
        chosen_categories = st.sidebar.multiselect("Catégories de questions", formatted_categories, default=formatted_categories[0:2])
        chosen_original_categories = [category_mapping[category] for category in chosen_categories]

        var4_1 = st.sidebar.selectbox("Choisissez une variable catégorielle pour le quatrième graphe",
                                                        options=variables,
                                                        index=0)

        
        #-----------------------------------------------------------------------

        st.header("Visualisations")
        Utils.newLines(1)
        st.header("Comparaison des données entre les années")

        Utils.newLines(4)

        #-----------------------------------------------------------------------

        # Ajout graphe1
        st.subheader("Graphe 1: Répartition des réponses moyennes par par une seule variable catégorielle et par année")
        st.write("Ce graphe montre la répartition des réponses moyennes en fonction d'une variable catégorielle sélectionnée (par exemple, le sexe, l'âge, la profession) pour deux années différentes. Les barres sont groupées par année et par valeur de la variable sélectionnée, permettant ainsi de comparer les réponses moyennes entre les deux années.")
        scatter_y_var = 'REPONSE_MOYENNE'
        grouped_bar1 = plot_grouped_bar1_with_year(data=combined_data,
                                            scatter_x_var=var1_1,
                                            scatter_y_var=scatter_y_var,
                                            color_var='YEAR',
                                            color_dict={'Année 1': 'Blue', 'Année 2': 'Teal'},
                                            year_var='YEAR')
        st.plotly_chart(grouped_bar1)
        Utils.newLines(4)

        #-----------------------------------------------------------------------

        # Ajout graphe2
        st.subheader("Graphe 2: Répartition des réponses moyennes par deux variables catégorielles et par année")
        st.write("Ce graphe montre la répartition des réponses moyennes en fonction de deux variables catégorielles sélectionnées (par exemple, le sexe et le secteur) pour deux années différentes. Les barres sont groupées par année, par première variable catégorielle et par deuxième variable catégorielle, permettant ainsi de comparer les réponses moyennes pour chaque combinaison de variables catégorielles entre les deux années.")
        if len(variables) > 1:
            grouped_bar2 = plot_grouped_bar2_with_year(data=combined_data,
                                                        scatter_x_var=var2_1,
                                                        scatter_y_var=scatter_y_var,
                                                        color_var=var2_2,
                                                        year_var='YEAR')

            st.plotly_chart(grouped_bar2)
        else:
            st.warning("Veuillez sélectionner plus d'une variable catégorielle.")
        Utils.newLines(4)

        #-----------------------------------------------------------------------

        # Ajout graphe3
        st.subheader("Graphe 3: Comparaison des réponses moyennes par catégorie de questions")
        st.write("Ce graphe montre la comparaison des réponses moyennes pour les catégories de questions sélectionnées (par exemple, CLIMAT SANTE SECURITE, PRATIQUES CARRIERE, COMMUNICATION) entre les deux années. Les barres sont groupées par année et par catégorie de question, permettant ainsi de comparer les réponses moyennes pour chaque catégorie de question entre les deux années.")
        grouped_bar3 = plot_grouped_bar3_by_categories_with_year(combined_data, chosen_original_categories, Utils.format_category_name, 'YEAR')
        st.plotly_chart(grouped_bar3)
        Utils.newLines(4)

        #-----------------------------------------------------------------------

        # Ajout graphe4
        st.subheader("Graphe 4: Comparaison des réponses moyennes par les catégories de questions et variable catégorielle")
        st.write("Ce graphe montre la comparaison des réponses moyennes pour les catégories de questions sélectionnées (par exemple, CLIMAT SANTE SECURITE, PRATIQUES CARRIERE, COMMUNICATION) en fonction d'une variable catégorielle sélectionnée (par exemple, le sexe, l'âge, la profession) pour deux années différentes. Les barres sont groupées par année, par catégorie de question et par variable catégorielle, permettant ainsi de comparer les réponses moyennes pour chaque combinaison de catégories de questions et de variables catégorielles entre les deux années.")
        grouped_bar4 = plot_grouped_bar4_by_categories_with_year(combined_data, chosen_original_categories, var4_1, Utils.format_category_name, 'YEAR')
        st.plotly_chart(grouped_bar4)


    elif ((uploaded_file1 is None) and (uploaded_file2 is not None)):
        st.warning("Veuillez importer un fichier CSV pour l'année 1.")

    elif ((uploaded_file2 is None) and (uploaded_file1 is not None)):
        st.warning("Veuillez importer un fichier CSV pour l'année 2.")

    else:
        st.warning("Veuillez importer un fichier CSV pour l'année 1 et un fichier CSV pour l'année 2.")
