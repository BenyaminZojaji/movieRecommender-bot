import pandas as pd

class Rec_sys:
    def __init__(self):
        self.movies_df = pd.read_csv('movies.csv')
        self.ratings_df = pd.read_csv('ratings.csv')
        self.movies_df['year'] = self.movies_df.title.str.extract('(\(\d\d\d\d\))',expand=False)
        self.movies_df['year'] = self.movies_df.year.str.extract('(\d\d\d\d)',expand=False)
        self.movies_df['title'] = self.movies_df.title.str.replace('(\(\d\d\d\d\))', '')
        self.movies_df['title'] = self.movies_df['title'].apply(lambda x: x.strip())
        self.movies_df['genres'] = self.movies_df.genres.str.split('|')
        self.moviesWithGenres_df = self.movies_df.copy()
        for index, row in self.movies_df.iterrows():
            for genre in row['genres']:
                self.moviesWithGenres_df.at[index, genre] = 1
        self.moviesWithGenres_df = self.moviesWithGenres_df.fillna(0)
        self.ratings_df = self.ratings_df.drop('timestamp', 1)

    def rs_preprocess(self, message):
        msg_line = message.split('\n')
        movies = []
        ratings = []
        for line in msg_line:
            try:
                mv, rt = line.split('-')
                movies.append(mv.title())
                ratings.append(rt)
            except: # happens when user forgot to give rates.
                return False
        df = pd.DataFrame(list(zip(movies, ratings)), columns =['title', 'rating'])
        return df

    def recommender_system(self, message):
        self.userInput = self.rs_preprocess(message)
        self.userInput['rating'] = pd.to_numeric(self.userInput['rating'], errors='coerce')
        try:
            self.inputMovies = pd.DataFrame(self.userInput)
            self.inputId = self.movies_df[self.movies_df['title'].isin(self.inputMovies['title'].tolist())]
            self.inputMovies = pd.merge(self.inputId, self.inputMovies)
            self.inputMovies = self.inputMovies.drop('genres', 1).drop('year', 1)
            self.userMovies = self.moviesWithGenres_df[self.moviesWithGenres_df['movieId'].isin(self.inputMovies['movieId'].tolist())]
            self.userMovies = self.userMovies.reset_index(drop=True)
            self.userGenreTable = self.userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
            self.userProfile = self.userGenreTable.transpose().dot(self.inputMovies['rating'])
            self.genreTable = self.moviesWithGenres_df.set_index(self.moviesWithGenres_df['movieId'])
            self.genreTable = self.genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)
            self.recommendationTable_df = ((self.genreTable*self.userProfile).sum(axis=1))/(self.userProfile.sum())
            self.recommendationTable_df = self.recommendationTable_df.sort_values(ascending=False)
            self.result = self.movies_df.loc[self.movies_df['movieId'].isin(self.recommendationTable_df.head(20).keys())]
            return '\n'.join(self.result['title'].tolist())
        except: # when pre-process return False
            return False
#a=Rec_sys()
#a.recommender_system('Toy Story-3.5\nPulp Fiction-5\nAkira-4.5\nJumanji-2')