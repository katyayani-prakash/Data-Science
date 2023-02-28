#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import re
import math


# In[ ]:


##Data Collection##

#reading the contents of given file and storing it in a dataframe, df
df = pd.read_csv("C://Users//Katyayani//OneDrive//Desktop//Fall 21 Courses//COMP 598//A1//IRAhandle_tweets_1.csv")

#slicing the dataframe to include only first 10000 tweets
tweets = df[0:10000]

#filtering the dataframe to include only English tweets
eng_tweets = tweets.loc[tweets['language'] == "English"]

#filtering the English tweets further to filter out all tweets that contain a question mark
step1 = eng_tweets.loc[~eng_tweets['content'].str.contains('\?')]

print(step1)

#writing the contents of Data Collection phase onto step1.tsv file 
step1.to_csv("C://Users//Katyayani//OneDrive//Desktop//Fall 21 Courses//COMP 598//A1//step1.tsv",index=False,sep='\t')


# In[ ]:


##Data Annotation##

#creating a new column called 'trump_mention' that is initialized with False for all rows
step1['trump_mention'] = False

#defining the conditional statement for switching the value of 'trump_mention' to True
step1.loc[step1['content'].str.contains('[^a-zA-Z0-9]Trump'),'trump_mention'] = True
step1.head()

step2 = step1

#retaining only the required columns
step2 = step2[['tweet_id', 'publish_date', 'content', 'trump_mention']]

print(step2)
print(step2['trump_mention'])

#writing the contents of Data Annotation phase onto dataset.tsv file
step2.to_csv("C://Users//Katyayani//OneDrive//Desktop//Fall 21 Courses//COMP 598//A1//dataset.tsv",index=False,sep='\t')


# In[ ]:


##Analysis##

true_values = step2['trump_mention'].values.sum()
false_values = (~step2['trump_mention']).values.sum()

print(true_values,false_values)

frac_trump_mentions = ((true_values)/(true_values+false_values))
print(frac_trump_mentions)

#truncating the result to 3 decimal points
ftm = format(frac_trump_mentions, ".3f")
print(ftm)

# initialize list of lists
data = [['frac-trump-mentions', ftm]]
 
# Create the pandas DataFrame
df1 = pd.DataFrame(data, columns = ['result', 'value'])
 
# print dataframe.
print(df1)

#writing the contents of Analysis phase onto results.tsv file
df1.to_csv("C://Users//Katyayani//OneDrive//Desktop//Fall 21 Courses//COMP 598//A1//results.tsv",index=False,sep='\t')

