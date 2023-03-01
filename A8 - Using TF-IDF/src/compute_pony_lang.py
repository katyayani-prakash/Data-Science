import os,sys
import pathlib
import argparse
import json
import pandas as pd
from numpy import log10
# from math import log10

def get_word_used_by_num_ponies(df,ponies):
    df.insert(loc=0, column="words", value=(df.index))              #creating a new column 'words' that has same value as index
    df.reset_index(drop=True, inplace=True)                         #resetting index
    df['word_used_by_num_ponies'] = 0
    count = 0

    for index,row in df.iterrows():
        for pony in ponies:
            if(df[pony][index] != 0):
                count = count+1
        df['word_used_by_num_ponies'][index] = count
        count = 0  
    
    return df

def get_tf_idf(df,ponies):
    ## TF-IDF = (number of times pony uses word w) * log(6/(no. of ponies that use the word w)
    ## so, if "example" word is used by 2 ponies, and twilight sparkle uses it 10 times, then:
    ##TF-IDF(example, twilight_sparkle) = 10 * log(6/2)
    out = {}
    for pony in ponies:
        new_list = []
        df[f'tf_idf_{pony}'] = (df[pony] * (log10(6/(df['word_used_by_num_ponies']))))
        filtered_df = df[["words",f'tf_idf_{pony}']].sort_values(by=f'tf_idf_{pony}',ascending=False)
        new_list = df[f'tf_idf_{pony}'].to_list()
        out.update({pony:new_list})
    
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--input')
    parser.add_argument('-n','--num_of_words',type=int)
    args = parser.parse_args()

    num_of_words = args.num_of_words

    with open(args.input,'r') as f:
        infile = json.load(f)
    input_json = json.dumps(infile)

    df = pd.read_json(input_json)
    df = df.fillna(0)
    
    # "twilight sparkle", "applejack", "rarity", "pinkie pie", "rainbow dash", "fluttershy".
    ponies = ['twilight sparkle','applejack','rarity','pinkie pie','rainbow dash','fluttershy']

    df = get_word_used_by_num_ponies(df,ponies)
    
    # df.to_csv('task2.csv',index=False)

    tf_idf_count_list = get_tf_idf(df,ponies)

    # print(tf_idf_count_list)
 
    out = {}
    # list = df['words'].to_list()
    for pony in ponies:
        new_list = []
        df[f'tf_idf_{pony}'] = (df[pony] * (log10(6/(df['word_used_by_num_ponies']))))
        filtered_df = df[["words",f'tf_idf_{pony}']].sort_values(by=f'tf_idf_{pony}',ascending=False)
        list = filtered_df['words'].to_list()
        # print(filtered_df.head())     
        for i in range(num_of_words):
            try:
                new_list.append(list[i])
            except:
                new_list = []
        out.update({pony:new_list})

    out_json  = json.dumps(out,indent=4)
    print(out_json)   
    


if __name__ == "__main__":
    main()
