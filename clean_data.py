'''Cleans and merges imdb.title.basics and tn databases'''
import pandas as pd


def get_imdb():
    '''Retrieves cleaned imdb.title.basics dataframe'''
    # Import relevant imdb database
    df_imdb = pd.read_csv("./data/imdb.title.basics.csv")
    # Remove rows where genre is NaN
    df_imdb.dropna(subset=['genres'], inplace=True)
    # Split genres strings and create a list containing genre strings
    df_imdb.genres = df_imdb.genres.map(lambda x:
                                        str(x).split(","))
    # Create a list containing unique genres
    unique_genres = []
    for i in df_imdb.genres:
        for j in i:
            if j in unique_genres:
                continue
            else:
                unique_genres.append(j)
    # Create a dict containing unique genres as keys and lists
    # of one-hot encoding for movie genres as values
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
    # Add columns to dataframe of one-hot encoding of genres
    for genre in unique_genres:
        df_imdb[genre] = genre_dict[genre]
    # Make all column names snake_case
    new_columns = df_imdb.columns.map(lambda x: x.replace('-', '_').lower())
    df_imdb.columns = new_columns
    return df_imdb


def tn_movie_budgets(cutoff=1):
    '''Imports and cleans tn database'''
    # Import The Numbers movie budget database
    df_tn = pd.read_csv('data/tn.movie_budgets.csv')
    # Convert object in format $10,000 to float64 for domestic_gross column
    df_tn.domestic_gross = df_tn.domestic_gross.replace(
        '[$,]',
        '',
        regex=True
    ).astype(float)
    # Convert object in format $10,000 to float64 for worldwide_gross column
    df_tn.worldwide_gross = df_tn.worldwide_gross.replace(
        '[$,]',
        '',
        regex=True
    ).astype(float)
    # Convert object in format $10,000 to float64 for production_budget column
    df_tn.production_budget = df_tn.production_budget.replace(
        '[$,]',
        '',
        regex=True
    ).astype(float)
    # Create new df with only movies above the worldwide_gross cut-off
    df_tn_cutoff = df_tn.loc[df_tn['worldwide_gross'] > cutoff].copy()
    # Convert release_date to datetime data type
    df_tn_cutoff['release_date'] = pd.to_datetime(df_tn_cutoff.release_date)
    # Make new column with start year of movie
    df_tn_cutoff['start_year'] = df_tn_cutoff.release_date.dt.year
    return df_tn_cutoff


def movies_combined():
    '''Merge imdb and tn database'''
    # Import The numbers database and relevant imdb database
    df_tn = tn_movie_budgets()
    df_imdb = get_imdb()
    # Create new df joining df_tn and df_imdb on title and year
    df_comb = pd.merge(df_imdb, df_tn, how='inner',
                       left_on=['original_title', 'start_year'],
                       right_on=['movie', 'start_year'])
    # Drop duplicated except for longest movies
    # (removes many NaN and <30 minute cases)
    df_comb.sort_values(by='runtime_minutes', ascending=False)
    df_comb.drop_duplicates(subset='primary_title', keep='first', inplace=True)
    # Subset movies that have 2010 - 2018 start years
    df_comb = df_comb.loc[df_comb['start_year'] < 2019].copy()
    # Remove irrelevant genre columns
    df_comb.drop(columns=['news', 'adult', 'talk_show', 'reality_tv',
                          'game_show', 'short'], inplace=True)
    return df_comb


def movies_combined_cutoff(cutoff):
    '''Merge imdb and tn database'''
    # Import The numbers database and relevant imdb database
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
    # Subset movies that have 2010 - 2018 start years
    df_comb = df_comb.loc[df_comb['start_year'] < 2019]
    # Remove irrelevant genre columns
    df_comb.drop(columns=['news', 'adult', 'talk_show', 'reality_tv',
                          'game_show', 'short'], inplace=True)
    return df_comb
