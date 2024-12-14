import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
from django.conf import settings
import os
import requests
import json
import pickle

class AI:

    similarities = []
    pt = []
    isWorked = False
    readyToRecommend = False
    api_key = "AIzaSyBiephTv_bRABusQde8341QqHxkF4uxtto"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    isGeminiWorked = False
    geminiBooks = []
    cache_file = "recommendation_cache.pkl"

    @staticmethod
    def createRecommendationInstance():
        if not AI.isWorked:
            AI.isWorked = True
        else:
            return
        if os.path.exists(AI.cache_file):
            with open(AI.cache_file, "rb") as f:
                data = pickle.load(f)
                AI.pt = data["pt"]
                AI.similarities = data["similarities"]
                AI.isWorked = True
                AI.readyToRecommend = True
                print("Veriler önbellekten yüklendi.")
                return
        books_path = os.path.join(settings.BASE_DIR, 'datasets', 'Books.csv')
        ratings_path = os.path.join(settings.BASE_DIR, 'datasets', 'ratings.csv')
        users_path = os.path.join(settings.BASE_DIR, 'datasets', 'Users.csv')
        
        books = pd.read_csv(books_path)
        ratings = pd.read_csv(ratings_path)
        users = pd.read_csv(users_path)

        books.loc[187689, 'Book-Author'] = 'Downes, Larissa Anne'

        users.drop(columns=['Age'], inplace=True)

        books.loc[209538, 'Book-Author'] = 'Michael Teitelbbaum'
        books.loc[209538, 'Book-Title'] = 'DK Readers: The Story of the X-Men, How It All Began (Level 4: Proficient Readers)'
        books.loc[209538, 'Year-Of-Publication'] = 2000
        books.loc[209538, 'Publisher'] = 'DK Publishing Inc'

        books.loc[220731, 'Book-Title'] = "Peuple du ciel, suivi de 'Les Bergers'"
        books.loc[220731, 'Book-Author'] = 'Jean-Marie Gustave Le Clézio'
        books.loc[220731, 'Year-Of-Publication'] = 1990
        books.loc[220731, 'Publisher'] = 'Gallimard'

        books.loc[221678, 'Book-Title'] = 'DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)'
        books.loc[221678, 'Book-Author'] = 'James Buckley'
        books.loc[221678, 'Year-Of-Publication'] = 2000
        books.loc[221678, 'Publisher'] = 'DK Publishing Inc'

        books['Year-Of-Publication'] = books['Year-Of-Publication'].astype('int64')

        books['Year-Of-Publication'].value_counts().sort_index(ascending=False).iloc[:20]

        books[books['Year-Of-Publication']>2021][['Book-Title','Year-Of-Publication','Publisher','Book-Author']]

        books.loc[37487, 'Year-Of-Publication'] = 1991
        books.iloc[37487]

        books.loc[37487, 'Year-Of-Publication'] = 1991

        books.loc[55676, 'Year-Of-Publication'] = 2005

        books.loc[37487, 'Book-Author'] = 'Bruce Coville'

        books.loc[80264, 'Year-Of-Publication'] = 2003

        books.loc[192993, 'Year-Of-Publication'] = 2003

        books.loc[78168, 'Year-Of-Publication'] = 2001

        books.loc[97826, 'Year-Of-Publication'] = 1981

        books.loc[116053, 'Year-Of-Publication'] = 1995

        books.loc[118294, 'Year-Of-Publication'] = 2023

        books.loc[228173, 'Year-Of-Publication'] = 1987

        books.loc[240169, 'Year-Of-Publication'] = 1996

        books.loc[246842, 'Year-Of-Publication'] = 1925

        books.loc[255409, 'Year-Of-Publication'] = 1937

        books.loc[260974, 'Year-Of-Publication'] = 1991

        books['Year-Of-Publication'].value_counts().sort_index(ascending=False).iloc[:20]

        books[(books['Year-Of-Publication']<1400)&(books['Year-Of-Publication']>0)]

        books_year_rational = books[books['Year-Of-Publication']!=0]['Year-Of-Publication'].value_counts().sort_index(ascending=False).iloc[:20]

        books[books['Book-Author'].duplicated()]

        author_book_count = books['Book-Author'].value_counts()

        author_book_count = books[books['Book-Author']!= 'Not Applicable (Na )']
        author_book_count_top50 = author_book_count.groupby('Book-Author').count()['Book-Title'].sort_values(ascending=False).head(50)

        cool = sns.color_palette("cool", n_colors=len(author_book_count_top50.values))

        publishers = books['Publisher'].value_counts()

        top_50_publishers = publishers.sort_values(ascending=False)[:51]

        cool = sns.color_palette("cool", n_colors=len(author_book_count_top50.values))

        bookRating = pd.merge(ratings, books, on="ISBN")

        bookRating.drop(columns=['Image-URL-S','Image-URL-M','Image-URL-L'],inplace=True)

        averageRating = pd.DataFrame(bookRating.groupby('ISBN')['Book-Rating'].mean().round(1))
        averageRating.reset_index(inplace=True)

        averageRating.shape
        averageRating.rename(columns={'Book-Rating':'Average-Rating'}, inplace=True)

        averageRatingdf = pd.merge(bookRating, averageRating, on='ISBN')

        averageRatingOnly = averageRatingdf[['ISBN','Average-Rating']]

        averageRatingUnique = averageRatingOnly[['ISBN','Average-Rating']].drop_duplicates(subset=['ISBN'])

        ratingBooks = pd.merge(books, averageRatingUnique, on='ISBN', how='inner')

        books_with_rating = pd.merge(books, averageRatingUnique, on='ISBN')

        books_with_rating = books_with_rating[['ISBN','Book-Title','Book-Author','Average-Rating','Year-Of-Publication','Publisher','Image-URL-S','Image-URL-M','Image-URL-L']]

        books_with_rating.sort_values(by=['Average-Rating'], ascending=False).head(30)

        ratings_sorted = books_with_rating['Average-Rating'].value_counts().sort_index(ascending=False)

        top_20_ratings = books_with_rating['Average-Rating'].value_counts().drop(index=0.0).sort_values(ascending=False).head(20)

        ratings_books_merged = ratings.merge(books, on='ISBN')

        ratings_books_nonzero = ratings_books_merged[ratings_books_merged['Book-Rating']!=0]
        num_rating_df = ratings_books_nonzero.groupby('Book-Title').count()['Book-Rating'].sort_values(ascending=False).reset_index()
        num_rating_df.rename(columns={'Book-Rating':'Number-of-Ratings'}, inplace=True)

        avg_rating_df = ratings_books_nonzero.groupby('Book-Title').mean(numeric_only=True)['Book-Rating'].reset_index()
        avg_rating_df.rename(columns={'Book-Rating':'Average-Rating'}, inplace=True)

        popularity_df = pd.merge(num_rating_df, avg_rating_df, on='Book-Title')

        popularity_df_above_100 = popularity_df[popularity_df['Number-of-Ratings']>=100]
        popularity_df_above_50 = popularity_df[popularity_df['Number-of-Ratings'] >= 50]
        popularity_df_above_250 = popularity_df[popularity_df['Number-of-Ratings'] >= 250]
        popularity_df_above_100.sort_values(by='Average-Rating', ascending=False).head()

        # Defining a new function that can calculate the metric
        def calcWeightedRating(row, avgRating, numOfRatings, minThres, defRating):
            weightedRating = ((row[avgRating] * row[numOfRatings]) + (minThres * defRating))/(row[numOfRatings] + minThres)
            return weightedRating

        # For number of ratings above 100
        popularity_df_above_100 = popularity_df_above_100.copy()
        popularity_df_above_100['Weighted-Rating'] = popularity_df_above_100.apply(lambda x: calcWeightedRating(
            x, 'Average-Rating', 'Number-of-Ratings', 100, 5),axis=1)
        popularity_df_above_100.sort_values(
            'Weighted-Rating', ascending=False).head(20)

        # For number of ratings above 50
        popularity_df_above_50 = popularity_df_above_50.copy()
        popularity_df_above_50['Weighted-Rating'] = popularity_df_above_50.apply(lambda x: calcWeightedRating(
            x, 'Average-Rating', 'Number-of-Ratings', 50, 5), axis=1)
        popularity_df_above_50.sort_values(
            'Weighted-Rating', ascending=False).head(20)

        # For number of ratings above 250
        popularity_df_above_250 = popularity_df_above_250.copy()
        popularity_df_above_250['Weighted-Rating'] = popularity_df_above_250.apply(lambda x: calcWeightedRating(
            x, 'Average-Rating', 'Number-of-Ratings', 250, 5), axis=1)
        popularity_df_above_250.sort_values(
            'Weighted-Rating', ascending=False).head(20)

        popular_df_merge = pd.merge(popularity_df_above_100, books, on='Book-Title').drop_duplicates('Book-Title',keep='first')
        popular_df_merge = popular_df_merge.drop(columns=['Image-URL-S', 'Image-URL-L'])
        popular_df_merge.sort_values('Weighted-Rating', ascending=False).head(10)

        users_ratings_count = ratings_books_merged.groupby('User-ID').count()['ISBN']
        users_ratings_count = users_ratings_count.sort_values(ascending=False).reset_index()
        users_ratings_count.rename(columns={'ISBN':'No-of-Books-Rated'}, inplace=True)

        users_200 = users_ratings_count[users_ratings_count['No-of-Books-Rated']>=200]

        books_with_users_200 = pd.merge(users_200, ratings_books_merged, on='User-ID')

        books_ratings_count = ratings_books_merged.groupby('Book-Title').count()['ISBN'].sort_values(ascending=False).reset_index()
        books_ratings_count.rename(columns={'ISBN':'Number-of-Book-Ratings'}, inplace=True)

        books_ratings_50 = books_ratings_count[books_ratings_count['Number-of-Book-Ratings']>=50]

        filtered_books = pd.merge(books_ratings_50, books_with_users_200,  on='Book-Title')

        famous_books = filtered_books.groupby('Book-Title').count().reset_index()
        famous_books = famous_books['Book-Title']
        famous_books = books[books['Book-Title'].isin(famous_books)]
        famous_books = famous_books.copy()
        famous_books.drop_duplicates(subset=['Book-Title'], inplace=True, keep='first')

        AI.pt = filtered_books.pivot_table(index='Book-Title',columns='User-ID', values='Book-Rating')
        AI.pt.fillna(0, inplace=True)

        AI.similarities = cosine_similarity(AI.pt)

        with open(AI.cache_file, "wb") as f:
            pickle.dump({"pt": AI.pt, "similarities": AI.similarities}, f)

        AI.readyToRecommend = True

    @staticmethod
    def recommend(book_name):
        if not AI.readyToRecommend:
            return "NotReadyToRecommend"
        
        if book_name in AI.pt.index:
            index = np.where(AI.pt.index == book_name)[0][0]
            similar_books_list = sorted(
                list(enumerate(AI.similarities[index])), key=lambda x: x[1], reverse=True)[1:11]   
            books = []
            for book in similar_books_list:
                books.append(AI.pt.index[book[0]])   
            return books

        else:
            closest_book = process.extractOne(book_name, AI.pt.index)
            if closest_book and closest_book[1] > 50:  
                return AI.recommend(closest_book[0])  
            else:
                return None
    
    
    @staticmethod
    def getMostPopularBooksByCategories():
        if AI.isGeminiWorked:
            return AI.geminiBooks
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Can you give me 15 most popular books on nowadays. Your results should be like these Do not change the response type give me always like. do not add your speaks. give me information only. Description may contain author name minimum lengh 70 max lengh 80. Categorys only Science-Fiction, History, Self-Development and Fantastic. I will parse your data so i do not want to take any error.:  Title:XXX, Description:XXX, Category:XXX"
                        }
                    ]
                }
            ]
        }

        # İstek gönderme
        response = requests.post(
            AI.url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )

        # Yanıtı yazdırma
        if response.status_code == 200:
            response_data = response.json()
            AI.isGeminiWorked = True
            # Parse the response and extract books
            books = []
            # Extract the text content from response
            for candidate in response_data.get('candidates', []):
                content = candidate.get('content', {})
                for part in content.get('parts', []):
                    text = part.get('text', '')
                    if text:
                        for t in text.split("\n"):
                            if len(t)>0:
                                title = str(t).split("Title:")[1].split("Description:")[0].split(',')[0]
                                description = str(t).split("Description:")[1].split("Category:")[0]
                                category = str(t).split("Category:")[1]
         
                                books.append({"Title": title, "Description": description, "Category":category})

            AI.geminiBooks = books
            return books
        else:
            print(f"Error: {response.status_code}, {response.text}")

    @staticmethod
    def getBookInfo(bookTitle):
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Can you give me information about "+bookTitle+" titled book.Your results should be like these Do not change the response type give me always like. do not add your speaks. give me information only. Description may contain author name minimum lengh 60 max lengh 220. I will parse your data so i do not want to take any error. Obey this rules does not include any ', comma' different than format.::  Title:XXX, Description:XXX, Category:XXX"
                        }
                    ]
                }
            ]
        }

        # İstek gönderme
        response = requests.post(
            AI.url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )

        # Yanıtı yazdırma
        if response.status_code == 200:
            response_data = response.json()
            AI.isGeminiWorked = True

            # Extract the text content from response
            for candidate in response_data.get('candidates', []):
                content = candidate.get('content', {})
                for part in content.get('parts', []):
                    text = part.get('text', '')
                    title = str(text).split("Title:")[1].split("Description:")[0].split(',')[0]
                    description = str(text).split("Description:")[1].split("Category:")[0]
                    category = str(text).split("Category:")[1]

                    book = {"Title": title, "Description": description, "Category":category}
                    return book

        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "Error"
    
    @staticmethod
    def getBookInfoForRecommendedBook(bookTitle):
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Can you give me information about "+bookTitle+" titled book.Your results should be like these Do not change the response type give me always like. do not add your speaks. give me information only. Description may contain author name minimum lengh 60 max lengh 220. I will parse your data so i do not want to take any error. If you don't have answer give random datas same format.::  Title:XXX, Description:XXX, Category:XXX, Author:XXX, Rating:XXX"
                        }
                    ]
                }
            ]
        }

        # İstek gönderme
        response = requests.post(
            AI.url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )

        # Yanıtı yazdırma
        if response.status_code == 200:
            response_data = response.json()
            AI.isGeminiWorked = True

            # Extract the text content from response
            for candidate in response_data.get('candidates', []):
                content = candidate.get('content', {})
                for part in content.get('parts', []):
                    text = part.get('text', '')
                    print (text)
                    try:
                        title = str(text).split("Title:")[1].split("Description:")[0].split(',')[0]
                        description = str(text).split("Description:")[1].split("Category:")[0]
                        category = str(text).split("Category:")[1].split("Author:")[0]
                        author = str(text).split("Author:")[1].split("Rating:")[0]
                        rating = str(text).split("Rating:")[1].split("\n")[0]
                        book = {"Title": title, "Description": description, "Category":category, "Author":author, "Rating":rating}

                        print(book)
                        return book
                
                    except:
                        return {"Title": "No Title", "Description": "No Description", "Category": "No Category", "CoverImage": "No Cover Image", "Author": "No Author", "Rating": "No Rating"}

        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "Error"