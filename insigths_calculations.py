from scipy.stats import chi2_contingency





def calculate_chi2(df, variable, category):
    descriptors = set(df[variable].tolist())
    values = dict()
    for descriptor in descriptors:
        values[descriptor] = df.loc[df[variable] == descriptor][category].tolist()
    
    chi2, pvalue, dof, expected = chi2_contingency(list(values.values()))
    return pvalue
