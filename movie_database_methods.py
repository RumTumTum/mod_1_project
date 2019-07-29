"""Various methods to support the reading and analysis of movie databases

Includes methods to:
- Import movie databases
- Join movie databases

"""


import pandas as pd

def bom_movie_gross():
    #read in the files
    df = pd.read_csv('data/bom.movie_gross.csv')


    #Convert object in format $10,000 to float64
    df.foreign_gross = df.foreign_gross.replace(
        '[\$,]',
        '',
        regex=True
    ).astype(float)

    #add a worldwide_gross column
    df['worldwide_gross'] = df.foreign_gross + df.domestic_gross
    
    #add a movie column to match the column title in tn.movie db
    df['movie'] = df.title

    return df
    
    
def tn_movie_budgets(cutoff = 1):
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

    #Sort by revenue
    df = df.sort_values(
        by = 'worldwide_gross', 
        ascending = False)

    #When there are duplicates keep higher revenue record 
    df.drop_duplicates(
        subset= 'movie', 
        keep = 'first',
        inplace = True
    )

    #pending - convert date to date

    #create new df with only movies above the revenue cut-off
    df_cutoff = df[df['worldwide_gross'] > cutoff]
    
    #Cutoff captures xx% of total movie revenue
#     share_cutoff = df_cutoff['worldwide_gross'].sum() / df['worldwide_gross'].sum()
#     print( 'cutoff of ', cutoff, " USD captures ", round(share_cutoff,2)*100, "% of total revenue")

    #returns a cleaned and sorted tn_movie_budgets
    return df_cutoff

def movies_combined (df_1, df_IMDB):
    df = 1
    
    #Copies to avoid overwriting original df_TN
    df_TN = df_1.copy()
    
    #Set 'movie' as index
    df_TN.set_index('movie', inplace=True)
    
    # create new df joining df_TN and df_IMDB
    df = df_IMDB.join(
    df_TN,
    on = 'primary_title',
    how = 'inner')
    
    return df