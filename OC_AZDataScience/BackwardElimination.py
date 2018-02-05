import statsmodels.formula.api as sm
from statsmodels.api import add_constant
from collections import defaultdict



####
dict_adjus_R = defaultdict(list)
####

def HighestPvalue(model, threshold):
    """
    returns true if all the values are below the threshold
    or returns the lowest p-value that is greater than 0.05
    """
    highest_pvalue = 0

    # for loops through the p-values of all the variables
    for index, current_pvalue in model.pvalues.items():
        # store the value of the greatest p-value
        if current_pvalue > highest_pvalue:
            highest_pvalue = current_pvalue
            highest_index = index

    if highest_pvalue > threshold: return highest_index
    else: return True

def CreateLinearReg(x, y):
    """
    returns the linear regression
    """
    X2 = add_constant(x)
    est = sm.OLS(y, X2)
    est2 = est.fit()
    return est2

def CreateLogReg(x,y):
    """
    returns the logistic regression
    """
    X2 = add_constant(x)
    est = sm.Logit(y, X2)
    est2 = est.fit()
    return est2

def BackwardElimination(Xs, y, stats_signf, model):
    """
    only returns the models if all the p-values are below the threshold
    if not, its a recursive model that will continue to use the function
    """


    if model == 'Linear':
        model_info = CreateLinearReg(Xs, y)
        #dict_adjus_R[len(Xs.columns)].append([Xs.columns, model_info.rsquared_adj])

    elif model == 'Logistic':
        model_info = CreateLogReg(Xs, y)

    p_results = HighestPvalue(model_info, stats_signf)

    if p_results is True: return model_info,

    else:
        Xs.drop(p_results, axis=1, inplace=True)
        BackwardElimination(Xs, y, stats_signf, model)
