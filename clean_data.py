'''Cleans and merges imdb.title.basics and tn databases'''
import pandas as pd


def get_imdb():
    '''Retrieves cleaned imdb.title.basics dataframe'''
    df_imdb = pd.read_csv("./data/imdb.title.basics.csv")
    # Remove rows where genre is NaN
    df_imdb.dropna(subset=['genres'], inplace=True)
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
    new_columns = df_imdb.columns.map(lambda x: x.replace('-', '_').lower())
    df_imdb.columns = new_columns
    return df_imdb


def tn_movie_budgets(cutoff=1):
    '''Imports and cleans tn database'''
    df_tn = pd.read_csv('data/tn.movie_budgets.csv')
    # Convert object in format $10,000 to float64
    df_tn.domestic_gross = df_tn.domestic_gross.replace(
        '[$,]',
        '',
        regex=True
    ).astype(float)
    # Convert object in format $10,000 to float64
    df_tn.worldwide_gross = df_tn.worldwide_gross.replace(
        '[$,]',
        '',
        regex=True
    ).astype(float)
    # Convert object in format $10,000 to float64
    df_tn.production_budget = df_tn.production_budget.replace(
        '[$,]',
        '',
        regex=True
    ).astype(float)
    # Convert date to date
    df_tn_cutoff = df_tn.loc[df_tn['worldwide_gross'] > cutoff].copy()
    # Create new df with only movies above the revenue cut-off
    df_tn_cutoff['release_date'] = pd.to_datetime(df_tn_cutoff.release_date)
    df_tn_cutoff['start_year'] = df_tn_cutoff.release_date.dt.year
    # Return a cleaned and sorted tn_movie_budgets
    return df_tn_cutoff


def movies_combined():
    '''Merge imdb and tn database'''
    df_tn = tn_movie_budgets()
    df_imdb = get_imdb()
    # Create new df joining df_TN and df_IMDB on movie title and year
    df_comb = pd.merge(df_imdb, df_tn, how='inner',
                       left_on=['original_title', 'start_year'],
                       right_on=['movie', 'start_year'])
    # Drop duplicated except for longest movies
    # (removes many NaN and <30 minute cases)
    df_comb.sort_values(by='runtime_minutes', ascending=False)
    df_comb.drop_duplicates(subset='primary_title', keep='first', inplace=True)
    # Only take movies that have been released and had time to make money
    df_comb = df_comb.loc[df_comb['start_year'] < 2019].copy()
    # Remove irrelevant rows
    df_comb.drop(columns=['news', 'adult', 'talk_show', 'reality_tv',
                          'game_show', 'short'], inplace=True)
    return df_comb


def movies_combined_cutoff(cutoff):
    '''Merge imdb and tn database'''
    df_tn = tn_movie_budgets(cutoff)
    df_imdb = get_imdb()
    # Create new df joining df_TN and df_IMDB on movie title and year
    df_comb = pd.merge(df_imdb, df_tn, how='inner',
                       left_on=['original_title', 'start_year'],
                       right_on=['movie', 'start_year'])
    # Drop duplicated except for longest movies
    # (remove many NaN and <30 minute cases)
    df_comb.sort_values(by='runtime_minutes', ascending=False)
    df_comb.drop_duplicates(subset='primary_title', keep='first', inplace=True)
    # Only take movies that have been released and had time to make money
    df_comb = df_comb.loc[df_comb['start_year'] < 2019]
    # Remove irrelevant rows
    df_comb.drop(columns=['news', 'adult', 'talk_show', 'reality_tv',
                          'game_show', 'short'], inplace=True)
    return df_comb
