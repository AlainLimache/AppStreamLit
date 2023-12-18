import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from plot_functions_une_annee import *
from Utils import Utils

def run_graphes_une_annee(authenticator, role, categories_questions, variables):
    # Configurer le style des graphiques
    sns.set(style="whitegrid", font_scale=1.1, rc={"figure.figsize": (10, 5)})
    plt.rcParams["figure.figsize"] = [10, 5]

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
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, delimiter=';', index_col=0)
        
        

        # Nouvelle colonne pour la réponse moyenne calculée
        data['REPONSE_MOYENNE'] = data[categories_questions].sum(axis=1) / len(categories_questions)

        Utils.newLines(3)
        st.write("### Données")
        st.write(data)
        Utils.newLines(1)

        # Formater les noms des gatégories
        formatted_categories = [Utils.format_category_name(category) for category in categories_questions]
        category_mapping = dict(zip(formatted_categories, categories_questions))

        Utils.add_separator()
        st.sidebar.title("Options")

        #-----------------------------------------------------------------------

        # Pour le grouped bar1: relation entre deux variables en utilisant des points
        st.sidebar.subheader("Grouped bar1")
        scatter_x_var = st.sidebar.selectbox("Variable catégorielle 1 pour le grouped bar1", variables, index=0)
        color_var = st.sidebar.selectbox("Variable catégorielle 2 (couleur) pour le grouped bar1", variables, index=0)

        Utils.add_separator()

        st.sidebar.subheader("Autres graphes")
        # Pour grouped bar2 & tous les autres graphes sauf grouped bar1 et Sankey
        chosen_categories = st.sidebar.multiselect("Catégories de questions", formatted_categories, default=formatted_categories[0:2])
        chosen_original_categories = [category_mapping[category] for category in chosen_categories]
        # Pour le grouped bar2 et Insight: Ajout d'une liste déroulante pour sélectionner la variable catégorielle dans la barre latérale
        grouped_bar_var = st.sidebar.selectbox("Variable catégorielle", variables, index=0)
        # Pour le plot_hist: distribution des valeurs
        nbins = st.sidebar.slider("Nombre de barres dans l'histogramme de ditribution des valeurs", min_value=1, max_value=50, value=5)
        Utils.add_separator()

        st.sidebar.subheader("Diagramme de Sankey")
        # Pour le diagramme de Sankey
        source_var_Sankey = st.sidebar.selectbox("Variable source", variables, index=0)
        target_var_Sankey = st.sidebar.selectbox("Variable cible", variables, index=0)
        color_mode_Sankey = st.sidebar.selectbox("Mode de couleur", ["Par source", "Par cible", "Par source-cible"], index=0)
        min_value_Sankey = st.sidebar.slider("Valeur minimale (réponse moyenne) pour afficher les sous-liens Sankey", 0.0, float(int(max(data['REPONSE_MOYENNE'])+1)), 0.0, step=0.05)
        Utils.add_separator()
        #-----------------------------------------------------------------------

        st.header("Visualisations")
        Utils.newLines(1)

        #-----------------------------------------------------------------------
        
        # Ajout de grouped bar1: Réponse moyenne pour deux variables en utilisant des barres groupées.
        st.subheader("Grouped Bar 1")
        st.write("Ce graphique montre les réponses moyennes pour deux variables catégorielles en utilisant des barres groupées. Chaque barre représente une valeur unique de la variable de couleur sélectionnée et la hauteur de chaque barre représente la réponse moyenne pour cette valeur de la variable de couleur. L'axe horizontal représente la variable x et l'axe vertical représente la réponse moyenne. Les couleurs représentent les différentes valeurs uniques de la variable de couleur. Les axes sont titrés avec les noms des variables x et de couleur.")
        scatter_y_var = 'REPONSE_MOYENNE'
        unique_values = data[color_var].unique()
        colors = plt.cm.get_cmap('tab10', len(unique_values))
        color_dict = {value: colors(index) for index, value in enumerate(unique_values)}
        fig_grouped_bar1 = plot_grouped_bar1(data, scatter_x_var, scatter_y_var, color_var, color_dict)
        st.plotly_chart(fig_grouped_bar1)
        Utils.newLines(5)

        #-----------------------------------------------------------------------

        # Ajout du graphique de réponse moyenne par des catégories
        st.subheader("Réponse moyenne par des catégories de questions")
        st.write("Ce graphique montre la réponse moyenne pour chaque catégorie de questions sélectionnée. Les barres représentent la réponse moyenne et les étiquettes à l'extérieur des barres représentent la valeur exacte de la réponse moyenne pour chaque catégorie de questions. Les axes représentent les catégories de questions sur l'axe x et la réponse moyenne sur l'axe y.")
        fig2 = plot_bar(data, chosen_original_categories, Utils.format_category_name)
        st.plotly_chart(fig2)
        Utils.newLines(5)

        #-----------------------------------------------------------------------
        
        # Ajout de grouped bar2: Réponse moyenne par chaque variable catégorielle
        st.subheader("Grouped bar 2")
        st.write("Ce graphe montre la réponse moyenne à chaque catégorie de questions pour chaque variable catégorielle (exemple: sexe, secteur..). Chaque variable catégorielle est représentée par des barres, et chaque barre est associé à une catégorie de question. La hauteur de chaque bar correspond à la réponse moyenne pour cette catégorie de questions pour cette variable catégorielle. Les couleurs représentent les différentes valeurs uniques de la variable catégorielle. Le nombre de barres dépend du nombre de valeurs uniques dans la variable catégorielle sélectionnée. Les axes représentent la variable catégorielle sur l'axe x et la réponse moyenne sur l'axe y.")
        # Générez un dictionnaire de couleurs pour les valeurs uniques de la variable catégorielle sélectionnée
        unique_grouped_bar_values = data[grouped_bar_var].unique()
        grouped_bar_colors = plt.cm.get_cmap('tab10', len(unique_grouped_bar_values))
        grouped_bar_color_dict = {value: grouped_bar_colors(index) for index, value in enumerate(unique_grouped_bar_values)}
        fig_grouped_bar2 = plot_grouped_bar2(data, chosen_original_categories, grouped_bar_var, Utils.format_category_name, grouped_bar_color_dict)
        st.plotly_chart(fig_grouped_bar2)
        Utils.newLines(5)

        #-----------------------------------------------------------------------

        #  Il est possible d'automatiser la recherche d'insights en fonction de critères spécifiques,
        #  tels que le diplôme ou l'âge. Pour ce faire, il faut utiliser des algorithmes de data mining 
        #  ou d'apprentissage automatique pour identifier les différences significatives entre les 
        #  différentes catégories. Par exemple, on peut utiliser une analyse de variance pour tester si 
        #  les différences observées entre les groupes sont significatives. Une fois les différences 
        #  significatives identifiées, on peut les présenter à l'utilisateur sous forme de graphiques 
        #  ou de tableaux pour permettre une analyse plus approfondie.

        # Ajout du graphique des insights
        st.subheader("Insights")
        st.write(f"Ce graphique montre les différences entre la moyenne de chaque groupe de {grouped_bar_var} et la moyenne globale pour chaque catégorie de questions. Il met en évidence les différences entre les moyennes de chaque groupe (par exemple, niveaux de diplôme) et la moyenne globale pour chaque catégorie de questions. Il permet d'identifier rapidement les tendances et les variations spécifiques à un groupe.")
        fig_insights = plot_insights(data, chosen_original_categories, grouped_bar_var, Utils.format_category_name)
        st.plotly_chart(fig_insights)
        st.write("**Axe des x**: Représente les différents groupes définis par une variable choisie (par exemple, niveaux de diplôme).")
        st.write("**Axe des y**: Indique la différence par rapport à la moyenne globale pour chaque catégorie de questions.")
        st.write("**Barres**: Représentent la différence par rapport à la moyenne globale pour chaque catégorie de questions et chaque groupe. Les barres sont colorées selon les catégories de questions.")
        st.write("**Légende**: Indique les catégories de questions et les couleurs correspondantes des barres. Vous pouvez cliquer sur les éléments de la légende pour afficher ou masquer les données sur le graphique.")
        Utils.newLines(5)

        #-----------------------------------------------------------------------

        # Ajout du graphique pour la contribution de chaque catégorie à la réponse moyenne
        st.subheader("Contribution des catégories de questions")
        st.write("Ce graphique montre la contribution de chaque catégorie de questions à la réponse moyenne.")
        st.write("Les pourcentages sont calculés en prenant la moyenne des réponses pour chaque catégorie de question, puis en divisant chaque valeur par la somme de toutes les valeurs moyennes pour obtenir les pourcentages. Les catégories ayant des valeurs inférieures à 1% sont regroupées sous une seule catégorie 'Autres' afin d'améliorer la lisibilité du graphique.")
        fig_pie = plot_pie(data, chosen_original_categories, Utils.format_category_name)
        st.plotly_chart(fig_pie)
        Utils.newLines(5)
        
        #-----------------------------------------------------------------------

        # Ajout du graphique de la distribution des valeurs pour chaque catégorie
        st.subheader("Distribution des valeurs pour chaque catégorie de questions")
        st.write("Ce graphique montre la distribution des valeurs pour les différentes catégories de questions sélectionnées. Les catégories de questions sont affichées sur l'axe des x, tandis que l'axe des y montre la fréquence des valeurs pour chaque catégorie. Les barres empilées représentent les différentes valeurs pour chaque catégorie, et la transparence des barres permet de visualiser les valeurs qui se chevauchent..")
        st.write("**Nombre de barres**: on peut choisir le nombre de bins (barres) à afficher à l'aide du slider")
        fig_hist = plot_hist(data, chosen_original_categories, Utils.format_category_name, nbins)
        st.plotly_chart(fig_hist, use_container_width=True)
        Utils.newLines(5)

        #-----------------------------------------------------------------------

        # Ajout du graphique en boîte (box plot) pour chaque catégorie
        st.subheader("Box plot pour chaque catégorie de questions")
        st.write("Ce graphique montre la répartition des valeurs (médiane, quartiles, valeurs extrêmes) pour chaque catégorie de questions.")
        fig_box = plot_box(data, chosen_original_categories, Utils.format_category_name)
        st.plotly_chart(fig_box)
        Utils.newLines(5)

        #-----------------------------------------------------------------------

        # Ajout du Heatmap pour montrer les corrélations entre les catégories de questions
        st.subheader("Heatmap des corrélations entre les catégories de questions")
        st.write("Ce graphique montre les corrélations entre les catégories de questions.")
        fig_heatmap = plot_heatmap(data, chosen_original_categories, Utils.format_category_name)
        st.plotly_chart(fig_heatmap)
        Utils.newLines(5)

        #-----------------------------------------------------------------------

        # Ajout du diagramme de Sankey
        st.subheader("Diagramme de Sankey")
        st.write("Ce diagramme de Sankey montre comment les participants ont répondu aux questions dans notre enquête. Chaque catégorie est représentée par un nœud (un rectangle), et les liens entre les nœuds représentent les flux (les réponses des participants). Plus les flux sont importants, plus les liens sont épais. Vous pouvez sélectionner les variables source et cible pour le diagramme, ainsi que la variable de couleur pour distinguer les flux.")
        st.write("**Variable source**: Les sources sont les points de départ des flux dans le diagramme.")
        st.write("**Variable source**: Les cibles sont les points d'arrivée des flux dans le diagramme.")
        st.write("**Mode de couleur**: Vous avez le choix entre trois options : \"Par source\", \"Par cible\" et \"Par source-cible\". Si vous choisissez \"Par source\", les couleurs seront définies en fonction de la variable source. Si vous choisissez \"Par cible\", les couleurs seront définies en fonction de la variable cible. Si vous choisissez \"Par source-cible\", les couleurs seront définies en fonction de la combinaison source-cible.")
        st.write("**Valeur minimale (réponse moyenne) pour afficher les sous-liens Sankey**: vous pouvez définir une valeur minimale pour afficher les sous-liens dans le diagramme de Sankey. Si la valeur moyenne des réponses est inférieure à cette valeur, le sous-lien correspondant ne sera pas affiché dans le diagramme.")

        value_var = 'REPONSE_MOYENNE'
        filtered_data = data[data[value_var] >= min_value_Sankey]
        fig_sankey = plot_sankey(filtered_data, source_var_Sankey, target_var_Sankey, value_var, color_mode_Sankey)
        st.plotly_chart(fig_sankey)

        #-----------------------------------------------------------------------

    else:
        st.warning("Veuillez importer un fichier CSV.")
