import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
from Utils import Utils

def plot_grouped_bar1_with_year(data, scatter_x_var, scatter_y_var, color_var, color_dict, year_var):
    fig_grouped_bar = go.Figure()

    unique_years = data[year_var].unique()
    unique_values = data[color_var].unique()

    for year in unique_years:
        data_year = data[data[year_var] == year]
        for value in unique_values:
            data_subset = data_year[data_year[color_var] == value].groupby(scatter_x_var)[scatter_y_var].mean().reset_index()
            fig_grouped_bar.add_trace(go.Bar(x=data_subset[scatter_x_var],
                                             y=data_subset[scatter_y_var],
                                             marker=dict(color=Utils.convert_color_to_hex(color_dict[value])),
                                             name=f"{year}"))

    fig_grouped_bar.update_layout(title=f"Comparaison de la réponse moyenne par {scatter_x_var} entre les années",
                                   xaxis_title=scatter_x_var,
                                   yaxis_title="Réponse moyenne",
                                   legend_title=color_var,
                                   barmode='group',
                                   hovermode="closest",
                                   font=dict(size=14),
                                   margin=dict(t=100, l=50, r=50, b=50))

    fig_grouped_bar.update_layout(
        legend=dict(
            font=dict(size=12),
            title=dict(text="Année")
        )
    )

    return fig_grouped_bar                            


def plot_grouped_bar2_with_year(data, scatter_x_var, scatter_y_var, color_var, year_var):
    fig_grouped_bar = go.Figure()

    unique_years = data[year_var].unique()
    unique_values = data[color_var].unique()

    for year in unique_years:
        data_year = data[data[year_var] == year]
        for value in unique_values:
            data_subset = data_year[data_year[color_var] == value].groupby(scatter_x_var)[scatter_y_var].mean().reset_index()
            fig_grouped_bar.add_trace(go.Bar(x=data_subset[scatter_x_var],
                                             y=data_subset[scatter_y_var],
                                             name=f"{year} - {value}"))

    fig_grouped_bar.update_layout(title=f"Comparaison de la réponse moyenne par {scatter_x_var} et par {color_var} entre les années",
                                   xaxis_title=scatter_x_var,
                                   yaxis_title="Réponse moyenne",
                                   legend_title=year_var,
                                   barmode='group',
                                   hovermode="closest",
                                   font=dict(size=14),
                                   margin=dict(t=100, l=50, r=50, b=50))

    fig_grouped_bar.update_layout(
        legend=dict(
            font=dict(size=12),
            title=dict(text="Année - " + f"{color_var}")
        )
    )

    return fig_grouped_bar


def plot_grouped_bar3_by_categories_with_year(data, chosen_original_categories, format_category_name, year_var):
    mean_data = data.groupby(year_var)[chosen_original_categories].mean().reset_index()

    color_dict = {'Année 1': 'blue', 'Année 2': 'Teal'}

    df = pd.melt(mean_data, id_vars=[year_var], value_vars=chosen_original_categories,
                 var_name='category', value_name='mean')

    fig3 = px.bar(df, x='category', y='mean', text='mean', color=year_var, barmode='group', color_discrete_map=color_dict)

    fig3.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig3.update_layout(
        title="Réponse moyenne par les catégories de questions sélectionnées et par année",
        xaxis_title="Catégories",
        yaxis_title="Réponse moyenne",
        xaxis_tickangle=-45,
        xaxis_tickvals=list(range(len(chosen_original_categories))),
        xaxis_ticktext=[format_category_name(category) for category in chosen_original_categories],
        legend=dict(
            font=dict(size=12),
            title=dict(text="Année")
        )
    )

    return fig3


def plot_grouped_bar4_by_categories_with_year(data, categories, groupby_var, format_category_name, year_var):
    grouped_data = data.groupby([year_var, groupby_var])[categories].mean().reset_index()
    df = pd.melt(grouped_data, id_vars=[year_var, groupby_var], value_vars=categories,
                 var_name='category', value_name='Réponse moyenne')

    color_dict = {'Année 1': 'blue', 'Année 2': 'Teal'}

    fig_grouped_bar4 = px.bar(df, x='category', y='Réponse moyenne', text='Réponse moyenne', color=year_var, facet_row=groupby_var, barmode='group', color_discrete_map=color_dict)

    fig_grouped_bar4.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_grouped_bar4.update_layout(
        title="Réponse moyenne par les catégories de questions sélectionnées et par variable catégorielle pour les deux années",
        xaxis_title="Catégories",
        yaxis_title="Réponse moyenne",
        xaxis_tickangle=-45,
        xaxis_tickvals=list(range(len(categories))),
        xaxis_ticktext=[format_category_name(category) for category in categories],
        legend=dict(
            font=dict(size=12),
            title=dict(text="Année")
        )
    )

    return fig_grouped_bar4

