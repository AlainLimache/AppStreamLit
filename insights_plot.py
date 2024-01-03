import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
from Utils import Utils

# Ajout de grouped bar1: Réponse moyenne pour deux variables en utilisant des barres groupées.
def plot_grouped_bar1_test(data, scatter_x_var, scatter_y_var, color_var, color_dict):
    fig_grouped_bar = go.Figure()

    unique_values = data[color_var].unique()

    for value in unique_values:
        data_subset = data[data[color_var] == value].groupby(scatter_x_var)[scatter_y_var].mean().reset_index()
        fig_grouped_bar.add_trace(go.Bar(x=data_subset[scatter_x_var],
                                         y=data_subset[scatter_y_var],
                                         name=value))

    fig_grouped_bar.update_layout(title=f"Réponse moyenne pour {scatter_x_var} et {color_var}",
                                   xaxis_title=scatter_x_var,
                                   yaxis_title="Réponse moyenne",
                                   legend_title=color_var,
                                   barmode='group',
                                   hovermode="closest")
    return fig_grouped_bar


def plot_linechart(data, descriptor, awnser):
    """
    Plot a linechart for the given data, descriptor and awnser.
    Parameters :
        data : dataframe
        descriptor : string
        awnser : string    
    """
    # Variable to stock the repartition of answers for each descriptor
    data_per_descriptor = dict()

    # For each descriptor, we create a dataframe with the repartition of answers
    for desc in data[descriptor].unique():
        # Get the total number of answers for the descriptor
        total_awnsers = len(data.loc[data[descriptor] == desc][awnser])

        # Get the repartition of answers for the descriptor
        df = pd.DataFrame(data.loc[data[descriptor] == desc][awnser].value_counts()*100/total_awnsers)
        df = df.reset_index()
        df.columns = [awnser, "count"]
        # Sort the dataframe by the awnser
        df = df.sort_values(by=[awnser])
        # Add the dataframe to the dictionary
        data_per_descriptor[desc] = df

    # Plot the linechart
    fig = go.Figure()

    for desc in data_per_descriptor.keys():
        fig.add_trace(go.Scatter(x=data_per_descriptor[desc][awnser], y=data_per_descriptor[desc]["count"], name=desc))
    
    fig.update_layout(
        title="Répartiton des réponses pour {} et {}".format(descriptor, awnser),
        xaxis_title="Réponse",
        yaxis_title="Pourcentage des réponses",
        legend_title="Descripteur"
    )

    return fig


def plot_barchart(data, descriptor, awnser):
    """
    Plot a barchart for the given data, descriptor and awnser.
    Parameters :
        data : dataframe
        descriptor : string
        awnser : string    
    """
    # Variable to stock the repartition of answers for each descriptor
    data_per_descriptor = dict()

    # For each descriptor, we create a dataframe with the repartition of answers
    for desc in data[descriptor].unique():
        # Get the total number of answers for the descriptor
        total_awnsers = len(data.loc[data[descriptor] == desc][awnser])

        # Get the repartition of answers for the descriptor
        df = pd.DataFrame(data.loc[data[descriptor] == desc][awnser].value_counts()*100/total_awnsers)
        df = df.reset_index()
        df.columns = [awnser, "count"]
        # Sort the dataframe by the awnser
        df = df.sort_values(by=[awnser])
        # Add the dataframe to the dictionary
        data_per_descriptor[desc] = df

    
    # Plot the barchart
    fig = go.Figure()

    for desc in data_per_descriptor.keys():
        fig.add_trace(go.Bar(x=data_per_descriptor[desc][awnser], y=data_per_descriptor[desc]["count"], name=desc))

    fig.update_layout(
        title="Répartiton des réponses pour {} et {}".format(descriptor, awnser),
        xaxis_title="Réponse",
        yaxis_title="Pourcentage des réponses",
        legend_title="Descripteur"
    )

    return fig