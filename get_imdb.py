import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_imdb():
    '''Retrieves cleaned imdb.title.basics dataframme'''
    imdb_title_basics = pd.read_csv("./data/imdb.title.basics.csv")
    imdb_title_basics = imdb_title_basics.loc[imdb_title_basics['genres'].isnull() == False]
    imdb_title_basics.genres = imdb_title_basics.genres.map(lambda x : str(x).split(","))
    return imdb_title_basics