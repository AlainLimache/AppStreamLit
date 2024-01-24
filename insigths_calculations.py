from scipy.stats import chi2_contingency, chisquare
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import scipy.stats as stats
import streamlit as st



@st.cache_data
def cochran_armitage_test(data, descriptor, answer):
    df = data[[descriptor, answer]]

    contingency_table = pd.crosstab(df[descriptor], df[answer])
    table = contingency_table.to_numpy()
    ctable = sm.stats.Table(table)
    result = ctable.test_ordinal_association()
    cochran_armitage_p_value = result.pvalue
    return cochran_armitage_p_value

@st.cache_data
def kruskal_test(data, descriptor, answer):
    df = data[[descriptor, answer]]
    groups = []
    for name, group in df.groupby(descriptor):
        groups.append(group[answer].tolist())
    kruskal_p_value = stats.kruskal(*groups).pvalue
    return kruskal_p_value


@st.cache_data
def chi2_test(data, descriptor, answer):
    df = data[[descriptor, answer]]

    contingency_table = pd.crosstab(df[descriptor], df[answer])
    table = contingency_table.to_numpy()
    chi2, pvalue, dof, expected = chi2_contingency(table)
    return pvalue




