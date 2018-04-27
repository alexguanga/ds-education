import statsmodels.formula.api as sm
from statsmodels.api import add_constant
from collections import defaultdict


dict_adjus_R = defaultdict(list)


'''Returns if all vals are below the threshold or the lowest-value'''
def HighestPvalue(model, threshold):
    highest_pvalue = 0

    # For loops through the p-values of all the variables
    for index, current_pvalue in model.pvalues.items():

        # Store the value of the greatest p-value
        if current_pvalue > highest_pvalue:
            highest_pvalue = current_pvalue
            highest_index = index

    if highest_pvalue > threshold: return highest_index
    else: return True

def CreateLinearReg(x, y):
    X2 = add_constant(x)
    est = sm.OLS(y, X2)
    est2 = est.fit()
    return est2

def CreateLogReg(x,y):
    X2 = add_constant(x)
    est = sm.Logit(y, X2)
    est2 = est.fit()
    return est2

def BackwardElimination(Xs, y, stats_signf, model='Linear'):
    if model == 'Linear':
        model_info = CreateLinearReg(Xs, y)

    elif model == 'Logistic':
        model_info = CreateLogReg(Xs, y)

    p_results = HighestPvalue(model_info, stats_signf)

    if p_results is True: return model_info,

    else:
        Xs.drop(p_results, axis=1, inplace=True)
        BackwardElimination(Xs, y, stats_signf, model)
