import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
from Utils import Utils

# Ajout de grouped bar1: Réponse moyenne pour deux variables en utilisant des barres groupées.
def group_data(data, descriptor, awnser):
    """
    Group data by descriptor and awnser.
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

    return data_per_descriptor


def display_data(data, insights, graph_type):
    for insight in insights:
            if graph_type == "Graph":
                fig = plot_linechart(data[[insight["variable"], insight["awnser"]]], insight["variable"], insight["awnser"])
            elif graph_type == "Boites":
                fig = plot_boxplot(data[[insight["variable"], insight["awnser"]]], insight["variable"], insight["awnser"])
            else:
                df = data[[insight["variable"], insight["awnser"]]]
                # Round values to nearest 1/3
                df[insight["awnser"]] = np.round(np.ceil(df[insight["awnser"]] * 3) / 3, 2)
                fig = plot_barchart(df, insight["variable"], insight["awnser"])
                        
            st.plotly_chart(fig)
            st.write("PValue : ", insight["pvalue"]) # TODO : Afficher la pvalue si besoin
            Utils.newLines(5)


def plot_linechart(data, descriptor, awnser):
    """
    Plot a linechart for the given data, descriptor and awnser.
    Parameters :
        data : dataframe
        descriptor : string
        awnser : string    
    """
    # Variable to stock the repartition of answers for each descriptor
    data_per_descriptor = group_data(data, descriptor, awnser)

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
    data_per_descriptor = group_data(data, descriptor, awnser)
    
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


def plot_boxplot(data, descriptor, awnser):
    """
    Plot a boxplot for the given data, descriptor and awnser.
    Parameters :
        data : dataframe
        descriptor : string
        awnser : string    
    """
    # Variable to stock the repartition of answers for each descriptor
    data_per_descriptor = group_data(data, descriptor, awnser)

    # Plot the boxplot
    fig = go.Figure()

    for desc in data_per_descriptor.keys():
        fig.add_trace(go.Box(x=data_per_descriptor[desc][awnser], name=desc))

    fig.update_layout(
        title="Répartiton des réponses pour {} et {}".format(descriptor, awnser),
        xaxis_title="Réponse",
        yaxis_title="Pourcentage des réponses",
        legend_title="Descripteur"
    )

    return fig