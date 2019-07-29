'''Retrieves cleaned imdb.title.basics dataframe'''

import pandas as pd


def get_imdb():
    '''Retrieves cleaned imdb.title.basics dataframe'''
    imdb_title_basics = pd.read_csv("./data/imdb.title.basics.csv")
    imdb_title_basics = imdb_title_basics.loc[imdb_title_basics['genres']
                                              .isnull() == False]
    imdb_title_basics.genres = imdb_title_basics.genres.map(lambda x:
                                                            str(x).split(","))
    unique_genres = []
    for i in imdb_title_basics.genres:
        for j in i:
            if j in unique_genres:
                continue
            else:
                unique_genres.append(j)
    genre_dict = {}
    for genre in unique_genres:
        genre_dict[genre] = []
    for genre in unique_genres:
        bool_list = []
        for movie in imdb_title_basics.genres:
            if genre in movie:
                bool_list.append('True')
            else:
                bool_list.append('False')
        genre_dict[genre] = bool_list
    for genre in unique_genres:
        imdb_title_basics[genre] = genre_dict[genre]
    return imdb_title_basics
