
import os, sys
import json
import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('input')
args = parser.parse_args()


file = open(args.input,'r')
lines = file.readlines()

df = pd.DataFrame()
for line in lines:
    record=json.loads(line)
    # append relevant data to dataframe
    df = df.append({
        'subreddit': record['data']['subreddit'],
        'title': record['data']['title'],
        'title_length': len(record['data']['title'])
    },ignore_index=True)


avg = (df['title_length'].sum())/(len(df['title_length']))
print(avg)