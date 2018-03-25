import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


"""
This program will create a dataframe with the information of the CAP Curve
It can also provide plot a graph with the given information
"""


def CapCurve(df):
    #structing the dataframe to be from largest to smallest
    updated_df = df.sort_values(by='Prediction', ascending=False)
    updated_df.reset_index(inplace=True)

    #creating a series that will be used as the total number of observations
    obs_series = pd.Series(np.arange(1,len(updated_df)+1))
    updated_df['Total_Records'] = obs_series

    #total number of observatiosn
    total_records = updated_df['Exited'].count()

    #total number of people who exited
    total_exited = updated_df['Exited'].sum()

    #percent of people exited
    percent_exited = total_exited/total_records

    #Building the dataframe that will help us build the CAP Curve
    #the percentage of the records to the total amount of records
    updated_df['Total_Percent'] = updated_df['Total_Records']/updated_df['Exited'].count()

    #if we were to randomly choose an observations, the percentage that it would
    #come out to be positive or 1
    updated_df['Random_Select'] = percent_exited * updated_df['Total_Records']

    #the percentage of the total people being selected as positive to the total people
    #who eventually become positive
    updated_df['Random_Select_Percent'] = updated_df['Random_Select']/total_exited

    #lastly, we need to create the prediction we made based on our model
    #inititate with the values of 0
    updated_df['Model_Select'] = 0
    sum_per_row = 0

    #for loop to captivate the sum per row
    for index, row in updated_df.iterrows():
        sum_per_row += updated_df.loc[index,"Exited"]
        updated_df.loc[index,"Model_Select"] = sum_per_row

    #percentage of the model of a positive classification
    updated_df['Model_Select_Percent'] = updated_df['Model_Select']/total_exited

    return updated_df



def PlotCapCurve(df):

    capcurve_df = CapCurve(df)

    plt.style.use('fivethirtyeight')

    fig1 = plt.figure(figsize=(10,8))
    ax1 = fig1.add_subplot(111)

    x = capcurve_df['Total_Percent']
    y1 = capcurve_df['Random_Select_Percent']
    y2 = capcurve_df['Model_Select_Percent']

    ax1.plot(x, y1)
    ax1.plot(x, y2)

    ax1.fill_between(x, y1, y2, facecolor='purple', interpolate=True)

    plt.title('CAP Curve')
    plt.xlabel('Total Percentage')
    plt.ylabel('Correct Percentage')
    plt.show()
