'''Cleans and merges imdb.title.basics and tn databases'''

import pandas as pd


def get_imdb():
    '''Retrieves cleaned imdb.title.basics dataframe'''
    df_imdb = pd.read_csv("./data/imdb.title.basics.csv")
    df_imdb = df_imdb.loc[df_imdb['genres']
                                              .isnull() == False]
    df_imdb.genres = df_imdb.genres.map(lambda x:
                                                            str(x).split(","))
    unique_genres = []
    for i in df_imdb.genres:
        for j in i:
            if j in unique_genres:
                continue
            else:
                unique_genres.append(j)
    genre_dict = {}
    for genre in unique_genres:
        genre_dict[genre] = []
    for genre in unique_genres:
        one_hot = []
        for movie in df_imdb.genres:
            if genre in movie:
                one_hot.append(1)
            else:
                one_hot.append(0)
        genre_dict[genre] = one_hot
    for genre in unique_genres:
        df_imdb[genre] = genre_dict[genre]
    new_columns = df_imdb.columns.map(lambda x: x.replace('-','_').lower())
    df_imdb.columns = new_columns
    return df_imdb
    
def tn_movie_budgets(cutoff = 1):
    '''Imports and cleans tn database'''
    
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
    #df.movie = df.movie.astype('str')
    
    #Sort by revenue
    df = df.sort_values(
        by = 'worldwide_gross', 
        ascending = False)

    #When there are duplicates keep higher revenue record 
#     df.drop_duplicates(
#         subset= 'movie', 
#         keep = 'first',
#         inplace = True
#     )

    #Convert date to date
    df_cutoff = df[df['worldwide_gross'] > cutoff]    
    
    #Cutoff captures xx% of total movie revenue
#     share_cutoff = df_cutoff['worldwide_gross'].sum() / df['worldwide_gross'].sum()
#     print( 'cutoff of ', cutoff, " USD captures ", round(share_cutoff,2)*100, "% of total revenue")

    #create new df with only movies above the revenue cut-off
    df_cutoff.loc[:,'release_date'] = pd.to_datetime(df_cutoff.release_date)
    df_cutoff['start_year'] = df_cutoff.release_date.dt.year
    
    #returns a cleaned and sorted tn_movie_budgets
    return df_cutoff

def movies_combined ():
    '''Merge imdb and tn database'''
    df_cutoff = tn_movie_budgets()
    df_imdb = get_imdb()
    df = 1    
    #Copies to avoid overwriting original df_TN
    df_TN = df_cutoff.copy()    
    #Set 'movie' as index
    df_TN.set_index('movie', inplace=True)    
    # create new df joining df_TN and df_IMDB
    df = pd.merge(df_imdb, df_TN,  how='inner', left_on=['original_title','start_year'], 
                  right_on = ['movie','start_year'])
    df.drop_duplicates(subset = 'primary_title', keep = 'first', inplace = True) 
    df = df.loc[df['start_year'] < 2019]
    df.drop(columns = ['news','adult','talk_show','reality_tv','game_show','short'], inplace = True)
    return df

def movies_combined_cutoff (cutoff = 0):
    '''Merge imdb and tn database'''
    df_cutoff = tn_movie_budgets(cutoff)
    df_imdb = get_imdb()
    df = 1    
    #Copies to avoid overwriting original df_TN
    df_TN = df_cutoff.copy()    
    #Set 'movie' as index
    df_TN.set_index('movie', inplace=True)    
    # create new df joining df_TN and df_IMDB
    df = pd.merge(df_imdb, df_TN,  how='inner', left_on=['original_title','start_year'], 
                  right_on = ['movie','start_year'])
    df.drop_duplicates(subset = 'primary_title', keep = 'first', inplace = True) 
    df = df.loc[df['start_year'] < 2019]
    df.drop(columns = ['news','adult','talk_show','reality_tv','game_show','short'], inplace = True)
    return df