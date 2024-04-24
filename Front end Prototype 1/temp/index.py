#!/usr/bin/env python
# coding: utf-8

# This is the real and final book prototype made with collaborative filtering. I used the same dataset as in the first book prototype, but used similar code to from the movies prototype to make this one.

# Dataset found from: https://www.kaggle.com/datasets/saurabhbagchi/books-dataset/data

# In[1]:


#Import libraries
import pandas as pd
import numpy as np
import re
import sys

# import ipywidgets as widgets
# from IPython.display import display

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# In[3]:


book_file = pd.read_csv("books_data/books.csv", sep=";", encoding='latin-1', on_bad_lines='skip')

# In[4]:


rating_file = pd.read_csv("books_data/ratings.csv", sep=";", encoding='latin-1', on_bad_lines='skip')

# In[5]:


vectorise = TfidfVectorizer(ngram_range=(1,2))
#turn title into matrix
matrix = vectorise.fit_transform(book_file["Book-Title"])

# In[6]:


#Create a search function, for when entering book title name
def search_title(title):
    vectored = vectorise.transform([title])
    similar = cosine_similarity(vectored, matrix).flatten()
    ten_most_similar_titles = np.argpartition(similar, -10)[-10:]
    final = book_file.iloc[ten_most_similar_titles][::-1]
    return final

# In[25]:


#Make the final recommendation function
def recommendation_function(bookId):
    #find users who liked the same book as book entered
    similar_user = rating_file[(rating_file["ISBN"] == bookId) & (rating_file["Book-Rating"] >= 5.5)]["User-ID"].unique()
    #find more books the user rated 6.5 or above
    user_likes = rating_file[(rating_file["User-ID"].isin(similar_user)) & (rating_file["Book-Rating"] >= 5.5)]["ISBN"]
    #turn the amount of the book counts into a percentage
    user_likes = user_likes.value_counts() / len(similar_user)
    #since there are alot of books liked, I only chose the ones where more than 20% of users liked
    user_likes = user_likes[user_likes > 0.01]
    
    #find all users who liked the book title
    users = rating_file[(rating_file["ISBN"].isin(user_likes.index)) & (rating_file["Book-Rating"] > 5.5)]
    #find percentage all users recommend each book
    users = users["ISBN"].value_counts() / len(users["User-ID"].unique())
    
    #now we need to compare the two percentages we have made
    #we will have a new table where the columns show how much each user likes a book and how much similar users like a book
    new_table = pd.concat([user_likes, users], axis=1)
    new_table.columns = ["user_likes", "users"]
    #Now we need to find the ratio between these two numbers
    new_table["ratio"] = new_table["user_likes"] / new_table["users"]
    #sort these ratios
    new_table = new_table.sort_values("ratio", ascending=False)
    
    #we need to get the titles of the highest ratio of books and return it
    return new_table.head(10).merge(book_file, left_index=True, right_on="ISBN")[["Book-Title", "Book-Author", "Year-Of-Publication", "Publisher"]]

# In[26]:


#Add a easier way for user to enter media - from user survey
# title_input = widgets.Text(
#     value="",
#     description="Enter Title:",
#     disabled=False
# )

# output_title = widgets.Output()

# def when_typing(text):
#     with output_title:
#         output_title.clear_output()
#         title = text["new"]
#         if len(title) >= 3:
#             output_book = search_title(title)
#             book_ID = output_book.iloc[0]["ISBN"]
#             display(recommendation_function(book_ID))

# title_input.observe(when_typing, names="value")
# display(title_input, output_title)

# In[ ]:


output_book = search_title(sys.argv[1])
book_ID = output_book.iloc[0]["ISBN"]
data = recommendation_function(book_ID)
print(data)
