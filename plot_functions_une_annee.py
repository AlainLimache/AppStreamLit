import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
from Utils import Utils

# Ajout de grouped bar1: Réponse moyenne pour deux variables en utilisant des barres groupées.
def plot_grouped_bar1(data, scatter_x_var, scatter_y_var, color_var, color_dict):
    fig_grouped_bar = go.Figure()

    unique_values = data[color_var].unique()

    for value in unique_values:
        data_subset = data[data[color_var] == value].groupby(scatter_x_var)[scatter_y_var].mean().reset_index()
        fig_grouped_bar.add_trace(go.Bar(x=data_subset[scatter_x_var],
                                         y=data_subset[scatter_y_var],
                                         marker=dict(color=Utils.convert_color_to_hex(color_dict[value])),
                                         name=value))

    fig_grouped_bar.update_layout(title=f"Réponse moyenne pour {scatter_x_var} et {color_var}",
                                   xaxis_title=scatter_x_var,
                                   yaxis_title="Réponse moyenne",
                                   legend_title=color_var,
                                   barmode='group',
                                   hovermode="closest")
    return fig_grouped_bar


# Ajout du graphique de réponse moyenne par des catégories
def plot_bar(data, chosen_original_categories, format_category_name):
    mean_data = data[chosen_original_categories].mean()
    fig2 = px.bar(mean_data.reset_index(), x='index', y=0, text=0)
    fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig2.update_layout(
        title="Réponse moyenne par les catégories de questions sélectionnées",
        xaxis_title="Catégories",
        yaxis_title="Réponse moyenne",
        xaxis_tickangle=-45,
        xaxis_tickvals=list(range(len(chosen_original_categories))),
        xaxis_ticktext=[format_category_name(category) for category in chosen_original_categories]
    )
    return fig2


# Ajout de grouped bar2: Réponse moyenne par chaque variable catégorielle
def plot_grouped_bar2(data, categories, groupby_var, format_category_name, color_dict):
    fig_grouped_bar = go.Figure()
    data_grouped = data.groupby(groupby_var)[categories].mean()

    ind = np.arange(len(categories))
    width = 0.35
    bar_positions = np.linspace(-width / 2, width / 2, len(color_dict))

    for index, (value, color) in enumerate(color_dict.items()):
        data_subset = data_grouped.loc[value]
        fig_grouped_bar.add_trace(go.Bar(x=[format_category_name(cat) for cat in categories],
                                         y=data_subset,
                                         marker=dict(color=Utils.convert_color_to_hex(color)),
                                         name=value,
                                         width=width / len(color_dict),
                                         offset=bar_positions[index]))

    fig_grouped_bar.update_layout(title=f"Réponse moyenne par chaque variable catégorielle",
                                   xaxis_title=groupby_var,
                                   yaxis_title="Réponse moyenne",
                                   legend_title=groupby_var,
                                   barmode='group',
                                   hovermode="closest")
    return fig_grouped_bar


# Ajout de Insights
def plot_insights(data, chosen_original_categories, groupby_var, format_category_name):
    data_grouped = data.groupby(groupby_var)[chosen_original_categories].mean()
    global_mean = data[chosen_original_categories].mean()
    differences = data_grouped - global_mean
    fig_insights = go.Figure()

    for category in chosen_original_categories:
        fig_insights.add_trace(go.Bar(x=differences.index,
                                      y=differences[category],
                                      name=format_category_name(category)))
    fig_insights.update_layout(title=f"Insights : Différences par rapport à la moyenne pour chaque {groupby_var}",
                               xaxis_title=groupby_var,
                               yaxis_title="Différence par rapport à la moyenne",
                               legend_title="Catégories de questions",
                               barmode='group',
                               hovermode="closest")
    return fig_insights

# Ajout du graphique pour la contribution de chaque catégorie à la réponse moyenne
def plot_pie(data, chosen_original_categories, format_category_name):
    #mean_data = data[chosen_original_categories].mean()
    mean_data = data[Utils.getCategories_question()].mean()
    formatted_mean_data = mean_data.rename(index=format_category_name)
    # Créer une nouvelle catégorie "Autres" pour les valeurs inférieures à 1%
    other_value = formatted_mean_data[formatted_mean_data < 0.01].sum()
    formatted_mean_data = formatted_mean_data[formatted_mean_data >= 0.01]
    formatted_mean_data['Autres'] = other_value
    fig_pie = go.Figure(data=[go.Pie(labels=formatted_mean_data.index, values=formatted_mean_data.values)])
    fig_pie.update_layout(title="Contribution de chaque catégorie à la réponse moyenne")
    return fig_pie

# Ajout du graphique de la distribution des valeurs pour chaque catégorie
def plot_hist(data, chosen_original_categories, format_category_name, nbins=10):
    data_hist = data[chosen_original_categories]
    fig_hist = go.Figure()
    for category in chosen_original_categories:
        fig_hist.add_trace(
            go.Histogram(x=data_hist[category], name=format_category_name(category), opacity=0.5, nbinsx=nbins)
        )
    fig_hist.update_layout(
        title="Distribution des valeurs pour les catégories de questions sélectionnées",
        xaxis_title="Valeur",
        yaxis_title="Fréquence",
        legend_title="Catégories",
        barmode='overlay',
        margin=dict(l=50, r=50, t=50, b=50),
        hovermode='x'
    )
    return fig_hist

# Ajout du graphique en boîte (box plot) pour chaque catégorie
def plot_box(data, chosen_categories, format_category_name):
    data_melted = data[chosen_categories].melt(var_name='Catégorie', value_name='Valeur')
    data_melted['Catégorie'] = data_melted['Catégorie'].apply(format_category_name)
    fig = px.box(data_melted, x='Catégorie', y='Valeur', color='Catégorie', color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(title="Box plot pour les catégories de questions sélectionnées",
                      xaxis_title="",
                      yaxis_title="Valeur",
                      xaxis_tickangle=-45,
                      xaxis_ticktext=list(data_melted['Catégorie'].unique()),
                      xaxis_tickvals=[f'Catégorie {i}' for i in range(len(data_melted['Catégorie'].unique()))])
    return fig


# Ajout du Heatmap pour montrer les corrélations entre les catégories de questions
def plot_heatmap(data, chosen_original_categories, format_category_name):
    # Récupérer les corrélations
    correlations = data[chosen_original_categories].corr()

    # Préparer les noms des catégories de questions
    formatted_labels = [format_category_name(category) for category in chosen_original_categories]

    # Créer la figure
    fig_heatmap = ff.create_annotated_heatmap(
    z=correlations.values,
    x=formatted_labels,
    y=formatted_labels,
    colorscale = ["Teal", "white", "lightcoral"],
    showscale=True,
    reversescale=True,
    annotation_text=correlations.round(2).values,
    font_colors=["white" if val < 0 else "black" for val in correlations.values.flatten()]
    )
    # Ajouter le titre
    fig_heatmap.update_layout(title_text='Corrélations entre les catégories de questions')
    # Modifier la position des labels sur l'axe x
    fig_heatmap.update_layout(xaxis_side='bottom')
    # Afficher la figure
    return fig_heatmap


# Ajout du Sankey
def plot_sankey(data, source_var, target_var, value_var, color_mode):
    source = data[source_var]
    target = data[target_var]
    value = data[value_var]

    unique_nodes = pd.concat([source, target]).unique()
    node_indices = {node: index for index, node in enumerate(unique_nodes)}

    # Créez un dictionnaire de couleurs en fonction du mode de couleur
    unique_colors = plt.cm.get_cmap('tab10', len(unique_nodes))
    if color_mode == "Par source":
        color_var = source_var
    elif color_mode == "Par cible":
        color_var = target_var
    else:
        color_var = source_var + "-" + target_var
        data[color_var] = data[source_var].astype(str) + "-" + data[target_var].astype(str)

    unique_values = data[color_var].unique()
    color_dict = {value: Utils.convert_color_to_hex(unique_colors(index)) for index, value in enumerate(unique_values)}

    sankey_link_colors = [color_dict[x] for x in data[color_var]]

    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=30,
            thickness=50,
            line=dict(color="black", width=0.5),
            label=unique_nodes,
        ),
        link=dict(
            source=[node_indices[src] for src in source],
            target=[node_indices[tgt] for tgt in target],
            value=value,
            color=sankey_link_colors
        )
    )])

    fig_sankey.update_layout(title_text="Diagramme de Sankey", font_size=12, legend=dict(orientation="v", x=1.05, xanchor="left", y=1, yanchor="top"))

    return fig_sankey


