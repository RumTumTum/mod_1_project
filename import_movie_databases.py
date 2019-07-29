"""Reads in movie database files. Methods output one Pandas Dataframe"""


import pandas as pd

def bom_movie_gross():
    #read in the files
    df = pd.read_csv('data/bom.movie_gross.csv')
    return df

    
def tn_movie_budgets():
    df = pd.read_csv('data/tn.movie_budgets.csv')

    #Convert object in format $10,000 to float64
    df.domestic_gross = df.domestic_gross.replace(
        '[\$,]',
        '',
        regex=True
    ).astype(float)

    #Convert object in format $10,000 to float64
    df.worldwide_gross = df.worldwide_gross.replace(
        '[\$,]',
        '',
        regex=True
    ).astype(float)

    #Convert object in format $10,000 to float64
    df.production_budget = df.production_budget.replace(
        '[\$,]',
        '',
        regex=True
    ).astype(float)
    
    #Convert object to str
#     df.movie = df.movie.astype('str')

    #pending - convert date to date
    #pending - convery name to string
    #having some difficulty converting to str
    
    return df