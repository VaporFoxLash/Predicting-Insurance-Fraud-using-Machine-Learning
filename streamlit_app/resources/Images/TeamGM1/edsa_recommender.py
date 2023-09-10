"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# image
from PIL import Image

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')

# App declaration


def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System", "Solution Overview", "About Us"]
    st.sidebar.write("## Autonomous Insights")
    image = Image.open("./resources/imgs/logo-bg.png")
    st.sidebar.image(image, width=200)

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        # st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.write('#### We give you best movie recommendations')
        st.write(
            '#### To receive recommendations, choose one of the recommender systems and your three favorite movies.')
        st.image('resources/imgs/Image_header.png', use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select a recommender system",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option', title_list[14930:15200])
        movie_2 = st.selectbox('Second Option', title_list[25055:25255])
        movie_3 = st.selectbox('Third Option', title_list[21100:21200])
        fav_movies = [movie_1, movie_2, movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")

        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except Exception as e:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")
                    st.error(f"Error: {e}")

    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        # st.write("Describe your winning approach on this page")
        st.write("### Challenge")
        st.write("There are innumerable alternatives available to movie lovers in the wide and varied world of movies. Finding the ideal movie that suits a person's tastes can be a difficult and time-consuming endeavor, though, because there is such a large selection. Movie recommendation systems have made an effort to address this problem, but many of them fall short by offering customers generic and unhelpful options.")
        st.write("## Our Winning Approach")
        st.write("We at Autonomous Insights have taken on the challenge of developing a unique movie recommendation system. For an unrivaled movie-watching experience, our successful strategy combines cutting-edge technology, creative algorithms, and a passion for movies.")
        st.write("## Advanced Machine Learning Techniques")
        st.write("Our recommendation engine for movies uses cutting-edge machine learning algorithms to examine a ton of movie-related data. By using collaborative filtering, we can use patterns in user viewing behavior to recommend movies to people who have similar likes. Additionally, our content-based filtering algorithms examine film qualities to suggest movies based on shared themes.")
        st.write("### Insights:")
        st.write("By using collaborative filtering, we draw on the collective knowledge of people with similar movie tastes, realizing that they frequently stumble across undiscovered masterpieces that suit their inclinations. Content-based filtering makes sure that suggestions don't just depend on what other people like; they also take into consideration particular aspects of movies that users like.")

        ratingNum = Image.open("resources/imgs/ratingNum.png")
        numRingsPerMovie = Image.open("resources/imgs/averageRating.png")
        output = Image.open("resources/imgs/output.png")
        wordCloud = Image.open("resources/imgs/wordCloud.png")

        st.write("#### Use of ratings for better recommendations")
        st.image(ratingNum, use_column_width=False,
                 clamp=False, width=720, output_format="JPEG")
        st.write("The top 20 genres in the dataset are shown in this bar chart. The number of films in each genre is indicated by the height of each bar. This graph sheds light on the variety of film genres included in the dataset as well as their relative popularity. such as. The tallest bar indicates that drama makes up the majority of the films in our collection.")
        st.image(wordCloud, use_column_width=False,
                 clamp=False, width=720, output_format="JPEG")

        st.image(output, use_column_width=False, clamp=False,
                 width=720, output_format="JPEG")

        st.write("The top 20 films with the highest average rating are shown in this bar graph. Each bar's height reflects the average rating for each film. This graph provides an overview of the most well-liked films in our collection, which might be helpful for promoting well-liked films to consumers. A movie with a high average rating but a low number of ratings might not be as dependable as a movie with a high average rating and a large number of ratings, so it's vital to take that into account as well.")
        st.image(numRingsPerMovie, use_column_width=False,
                 clamp=False, width=650, output_format="JPEG")

        st.write("The collaborative filtering method is the foundation of this solution for movie recommendation. The fundamental idea behind collaborative filtering is to use both collective user activity and individual user behavior to recommend products. The objects in this instance are movies.")
        st.write("The method makes use of the user-rated movie dataset from MovieLens. The ratings, movies, and users dataframes are combined through preprocessing of the data. It also includes further details like the director, runtime, budget, and storyline keywords for the movie.")
        st.write("The Singular Value Decomposition (SVD) model is the major one employed. The most common application of the SVD matrix factorization approach is to decrease the number of features in a data collection by switching from N- to K-dimensional space (where K=N). This")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.

    if page_selection == "About Us":
        st.write("## Our Vision")
        st.write("Our mission at Autonomous Insights is to improve your movie-watching experience by providing individualized and reliable movie suggestions. We think that everyone should be able to choose movies that suit their particular tastes and preferences in a simple and enjoyable way.   ")
        st.write("## Who We Are")
        st.write("Autonomous Insights is a passionate team of movie enthusiasts, data scientists, and AI experts dedicated to revolutionizing how you discover and enjoy movies. With a deep love for cinema and a profound understanding of artificial intelligence, we strive to bring you the ultimate movie recommendation platform.")
        st.write("## Our Technology")
        st.write("Our cutting-edge movie recommender system is powered by state-of-the-art machine learning algorithms and sophisticated deep learning models. We have meticulously curated and analyzed vast amounts of movie data to build an intelligent system that goes beyond generic recommendations.")
        st.write("## How It Works")
        st.write("Our online application has an easy-to-use interface and is built on the robust Streamlit framework. It uses a combination of content-based and collaborative filtering methods to provide you with tailored movie recommendations that best suit your preferences.")

        st.subheader("The Team")
        # Team images
        harmony = Image.open("resources/imgs/Team/harmony.png")
        emanuel = Image.open("resources/imgs/Team/emanuel.jpg")
        kgopotso = Image.open("resources/imgs/Team/kgopotso.jpg")
        lehlohonono = Image.open("resources/imgs/Team/lehlohonono.jpg")
        ndumiso = Image.open("resources/imgs/Team/ndumiso.jpg")
        phindulo = Image.open("resources/imgs/Team/phindulo.jpg")
        precious = Image.open("resources/imgs/Team/precious.jpg")
        yvonne = Image.open("resources/imgs/Team/yvonne.jpg")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(phindulo, use_column_width=False,
                     clamp=False, width=150, output_format="JPEG")
        with col2:
            st.image(harmony, use_column_width=False,
                     clamp=True, width=150, output_format="JPEG")
        with col3:
            st.image(lehlohonono, use_column_width=False,
                     clamp=False, width=150, output_format="JPEG")

        col4, col5, col6 = st.columns(3)

        with col4:
            st.write("Data Scientist")
            st.write("Ndumiso Nkosi")
            st.write("NdumisoNkosi@autiinsights.com")
        with col5:
            st.write("Machine Learning Engineer")
            st.write("Emmanuel Nkosi")
            st.write("EmmanuelNkosi@autiinsights.com")
        with col6:
            st.write("Data Engineer")
            st.write("Kgopotso Tlaka")
            st.write("KgopotsoTlaka@autiinsights.com")

        col7, col8, col9 = st.columns(3)

        with col7:
            st.image(ndumiso, use_column_width=False,
                     clamp=True, width=150, output_format="JPEG")
        with col8:
            st.image(emanuel, use_column_width=False,
                     clamp=True, width=150, output_format="JPEG")
        with col9:
            st.image(kgopotso, use_column_width=False,
                     clamp=True, width=150, output_format="JPEG")

        col10, col11, col12 = st.columns(3)

        with col10:
            st.write("Data Scientist")
            st.write("Ndumiso Nkosi")
            st.write("NdumisoNkosi@autiinsights.com")
        with col11:
            st.write("Machine Learning Engineer")
            st.write("Emmanuel Nkosi")
            st.write("EmmanuelNkosi@autiinsights.com")
        with col12:
            st.write("Data Engineer")
            st.write("Kgopotso Tlaka")
            st.write("KgopotsoTlaka@autiinsights.com")

        col13, col14 = st.columns(2)

        with col13:
            st.image(yvonne, use_column_width=False, clamp=True,
                     width=150, output_format="JPEG")

        with col14:
            st.image(precious, use_column_width=False,
                     clamp=True, width=150, output_format="JPEG")

        col15, col16 = st.columns(2)

        with col15:
            st.write("Data Analyst")
            st.write("Yvonne Malinga")
            st.write("YvonneMalinga@autiinsights.com")

        with col16:
            st.write("Data Analyst")
            st.write("Lesego Precious Sefike")
            st.write("LesegoPrecious @autiinsights.com")

        import os
        print(os.path.abspath("resources/imgs/EDSA_logo.png"))
        print(os.path.abspath("resources/imgs/EDSA_logo.png"))
        print(os.path.abspath("resources/imgs/EDSA_logo.png"))

        st.write("## Contact Us")
        st.write(
            "For inquiries or assistance, reach out to us at contact@autonomousinsights.com. We are open for business")

        st.write("Our website - autonomousinsights.com")


if __name__ == '__main__':
    main()
