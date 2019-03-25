import pandas as pd
import numpy as np

ratings_fields = ['userId', 'movieId', 'rating']
movies_fields = ['movieId', 'title']

ratings = pd.read_csv("./data/ratings.csv", encoding="ISO-8859-1", usecols=ratings_fields)
movies = pd.read_csv("./data/movies.csv", encoding="ISO-8859-1", usecols=movies_fields)
ratings = pd.merge(ratings, movies, on='movieId')

# empty dataframe for movie-movie afiniti score
movie_afiniti = pd.DataFrame(columns=[
    'base_movieId',
    'base_movieTitle',
    'associated_movieId',
    'associated_movieTitle',
    'afiniti_score'])


# get unique movies 
distinct_movies = np.unique(ratings['movieId'])

# movieId of movie viewer watched
ref_movie = 10
m_data = ratings[ratings['movieId'] == ref_movie]


# compare m1 with every other movie in distinct_movies 
for m1 in distinct_movies:

  if m1 == ref_movie:
    continue
  
  # count distinct viewers of m1
  m1_data = ratings[ratings['movieId'] == m1]
  m1_viewers = np.unique(m1_data['userId'])
  
  # find movies watched by same set of users to calculate afiniti score
  m2_viewers = np.intersect1d(m1_viewers, [m_data['userId']])
      
  # find common viewers of m2 and m1
  common_viewers = len(np.unique(m2_viewers))
  afiniti_score = float(common_viewers)/float(len(m1_viewers))

  # update movie_afiniti score dataframe
  movie_afiniti = movie_afiniti.append({
      "base_movieId": ref_movie,
      "base_movieTitle": m_data.loc[m_data['movieId'] == ref_movie, 'title'].iloc[0],
      "associated_movieId": m1,
      "associated_movieTitle": m1_data.loc[m1_data['movieId'] == m1, 'title'].iloc[0],
      "afiniti_score": afiniti_score
  }, ignore_index=True)

movie_afiniti = movie_afiniti.sort_values(['afiniti_score'], ascending=False)

# For better recommendations, set afiniti score threshold
similar_movies = movie_afiniti[(movie_afiniti['afiniti_score'] > 0.6)]

similar_movies.head(10)
