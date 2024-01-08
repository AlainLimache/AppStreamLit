from scipy.stats import chi2_contingency, chisquare
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import scipy.stats as stats




def calculate_chi2(data, descriptor, awnser):
    repartitions = list()

    for desc in data[descriptor].unique():
        # Get the total number of answers for the descriptor
        total_awnsers = len(data.loc[data[descriptor] == desc][awnser])

        # Get the repartition of answers for the descriptor
        df = pd.DataFrame(data.loc[data[descriptor] == desc][awnser].value_counts()/total_awnsers)
        df = df.reset_index()
        df.columns = [awnser, "count"]
        # Sort the dataframe by the awnser
        df = df.sort_values(by=[awnser])
        # Get the count colun as a list and add it to repartitions
        repartitions.append(df["count"].tolist())
    
    print(repartitions)
    try:
        chi2, pvalue, dof, expected = chi2_contingency(repartitions)
    except ValueError as e:
        print(e)
        pvalue = 1



    """
    descriptors = set(df[variable].tolist())
    values = dict()
    for descriptor in descriptors:
        values[descriptor] = df.loc[df[variable] == descriptor][category].tolist()
    
    chi2, pvalue, dof, expected = chi2_contingency(list(values.values()))
    """
    return pvalue


def cochran_armitage_test(data, descriptor, answer):
    df = data[[descriptor, answer]]

    contingency_table = pd.crosstab(df[descriptor], df[answer])
    table = contingency_table.to_numpy()
    ctable = sm.stats.Table(table)
    result = ctable.test_ordinal_association()
    cochran_armitage_p_value = result.pvalue
    return cochran_armitage_p_value








