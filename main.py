import streamlit as st
import instaloader
from instaloader import Profile
import pandas as pd
from PIL import Image
import plotly.express as px
import requests
from collections import Counter
import numpy as np
#from yt import get_continuous_chunks
from csv import writer
import subprocess
#from twitter import twitter
import os
from youtube import main
from datetime import datetime
import matplotlib.pyplot as plt


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def append_list_as_row(list_of_elem):
    file_name = 'main.csv'
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv filed
        csv_writer.writerow(list_of_elem)

def record_searcher(arg):
    answer = df[df['Number'] == arg].index
    final_answer = answer[0]
    return final_answer

analyzer = SentimentIntensityAnalyzer()

L = instaloader.Instaloader()
## L.login('aryxnsharma', '!!instagram!!')        # (login)

choices = ["YouTube", "Instagram"]
menu = st.sidebar.selectbox("Menu: ", choices)



if menu == "Instagram":
    st.title("Instagram Comments Sentiment")
    st.write("-----------------")
    post_id_final = st.text_input("Enter post link: ")
    #https://www.instagram.com/p/CJI5OyAsrW5/
    post_id = post_id_final[28:39]
    fetch = st.button("GET")
    if fetch:
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, post_id)
        comments = []
        pos_score = []
        neg_score = []
        neu_score = []
        final_list = []
        count = 0
        for i in post.get_comments():
            vs = analyzer.polarity_scores(i.text)
            if vs['pos'] > vs['neg'] and vs['neu']:
                final_list.append("Positive")
            elif vs['neu'] > vs['pos'] and vs['neg']:
                final_list.append("Neutral")
            elif vs['neg'] > vs['pos'] and vs['neu']:
                final_list.append("Negative")
            elif vs['compound'] > 0.3:
                final_list.append("Positive")
            elif vs['compound'] < 0.3:
                final_list.append("Negative")
            elif vs['compound'] == 0.3:
                final_list.append("Neutral")
            comments.append(str(i.text))
            if count > 10:
                break
            count += 1 
        dfnew = pd.DataFrame(final_list, columns=['Sentiment'])
        pie_fig = px.pie(dfnew, names="Sentiment")
        st.plotly_chart(pie_fig)
        #append_list_as_row(comments)
        for i in post.get_comments():
            answer = st.write(i.text)
    

elif menu == "YouTube":
    st.title("YouTube Comments Sentiment")
    st.write("--------------------")
    video_id_final = st.text_input("Enter video link: ")
    #https://www.youtube.com/watch?v=8KFi3ag9bEs
    video_id = video_id_final[32:43]
    fetch = st.button("GET")
    if fetch:
        st.write("------------------------")
        col1, col2 = st.beta_columns((1,2))
        answer = main(video_id)
        count = 0
        comments = []    
        final_list = []
        #st.write(answer)
        for i in answer['items']:
            one = i['snippet']
            two = one['topLevelComment']
            three = two['snippet']
            four = three['textOriginal']
            vs = analyzer.polarity_scores(four)
            if vs['pos'] > vs['neg'] and vs['neu']:
                final_list.append("Positive")
            elif vs['neu'] > vs['pos'] and vs['neg']:
                final_list.append("Neutral")
            elif vs['neg'] > vs['pos'] and vs['neu']:
                final_list.append("Negative")
            elif vs['compound'] > 0.3:
                final_list.append("Positive")
            elif vs['compound'] < 0.3:
                final_list.append("Negative")
            elif vs['compound'] == 0.3:
                final_list.append("Neutral")
            comments.append(str(four))
            if count > 25:
                break
            count += 1 
        dfnew = pd.DataFrame(final_list, columns=['Sentiment'])
        pie_fig = px.pie(dfnew, names="Sentiment")
        col2.plotly_chart(pie_fig)
        for i in comments:
            string_set = " ".join(comments)
            col1.write(i)

