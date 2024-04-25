#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

# In[2]:


pd.read_csv("spotify_millsongdata.csv")

# In[3]:


dataset = pd.read_csv("spotify_millsongdata.csv")

# In[4]:


#dataset['text'][0]

# In[5]:


dataset=dataset.sample(5000).drop('link', axis=1).reset_index(drop=True)

# In[6]:


#removing the \n from text
dataset['text'].str.lower().replace(r'^\w\s', ' ').replace(r'\n', ' ', regex = True)

# In[7]:


import nltk
#nltk.download('punkt')
from nltk.stem.porter import PorterStemmer

# In[8]:


test = PorterStemmer()

# In[9]:


def token(txt):
    token = nltk.word_tokenize(txt)
    tested = [test.stem(i) for i in token]
    return " ".join(tested)

# In[10]:


token("we are warriors, warriors")

# In[11]:


dataset['text'].apply(lambda x: token(x))

# In[12]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# In[13]:


tfid = TfidfVectorizer(analyzer='word', stop_words='english')

# In[14]:


matrix=tfid.fit_transform(dataset['text'])

# In[15]:


similarity = cosine_similarity(matrix)

# In[16]:


#similarity[0]

# In[17]:


dataset.tail(5)

# In[19]:


#dataset[dataset['song']=='Bad Attitude'].index[0]

# In[24]:


#Recommender Algorithm
def recommender(song_name):
    idx = dataset[dataset['song']==song_name].index[0]
    distance = sorted(list(enumerate(similarity[idx])), reverse=True, key = lambda x:x[1])
    song = []
    for s_id in distance[1:11]:
        song.append(dataset.iloc[s_id[0]].song)
    return song

# In[28]:


#recommender("When You're Smiling")
data = recommender(sys.argv[1])
print(data)

# In[ ]:



