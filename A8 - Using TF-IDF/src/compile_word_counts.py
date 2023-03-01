import os,sys
import argparse
import json
import pandas as pd
import pathlib
from pathlib import Path
import csv
import re


def filter_pony(df,column_name,pony_name):
    ## This function filters given dataframe to only include data for given pony
    ## and returns the filtered dataframe with new column dialog_new that is all lowercase and without punctuations
    df_filter = df.loc[df[column_name].str.fullmatch(pony_name, case=False)]

    punctuation = ['(', ')', '[', ']', ',', '-', '.', '?', '!', ':', ';', '#', '&']

    df_filter.insert(loc=4, column="dialog_new", value="")
    df_filter['dialog_new'] = df_filter['dialog'].str.lower() 

    for item in punctuation:
        df_filter['dialog_new'] = df_filter['dialog_new'].str.replace(item,' ',regex=True)

    return df_filter


def get_word_count(dataframe,words):
    ## This functions takes as input cleaned dataframe consisting of only one pony's dialogues, 
    ## and returns a dictionary of word and word_counts for that pony


    #creating a new dataframe that consists on 2 columns - word and word_count
    df_new = dataframe.dialog_new.str.split(expand=True).stack().value_counts().reset_index()
    df_new.rename(columns={'index': 'word', 0: 'word_count'}, inplace=True)

    #dropping all stopwords, numbers and non-alphabetic words
    for word in words:
        df_new = df_new.loc[(((df_new['word']) != word) & (df_new['word'].str.isalpha()))]

    #creating a dictionary with word column as key and word_count as value. Returning this dictionary
    df_dict = dict(zip(df_new['word'], df_new['word_count']))

    return df_dict

def get_stopwords():
    dr = os.path.dirname(__file__)

    #opening and reading stopwords.txt
    words = []
    with open(os.path.join(dr,'..','data','stopwords.txt')) as f:       #assumption: stopwords is always located at submission_template/data and code is in submission_template/src
        for curline in f:
            if curline.startswith("#"):                                 #ignoring all comment-lines in file
                pass
            else:
                words.append(curline.replace("\n",""))    

    return words


def main():
    #parsing command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--input')
    parser.add_argument('-o','--output')
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    ponies = ['twilight sparkle','applejack','rarity','pinkie pie','rainbow dash','fluttershy']

    words = get_stopwords()
    temp_out = {}                                                       #this dictionary will contain ALL words, before <5 filter
    for pony in ponies:
        try:
            filtered_df = filter_pony(df,'pony',pony)                   #filtering dataframe for each pony
            temp_out[pony] = {}                                         #creating an empty dictionary for each pony
            temp_out[pony] = get_word_count(filtered_df,words)          #storing returned dictionary from get_word_count method in the above empty dict
        except:
            temp_out[pony] = {}                                         #if pony does not exist, return blank dictionary for them

    
    ## Code snippet for filtering out words with <5 frequency across ALL speech acts

    temp_json = json.dumps(temp_out)

    df_out = pd.read_json(temp_json)
    df_out = df_out.fillna(0)                                           #replacing all NaN values with 0

    df_out.insert(loc=0, column="words", value=(df_out.index))          #creating a new column 'words' that has same value as index

    df_out.reset_index(drop=True, inplace=True)                         #resetting index

    df_out['sum_of_words'] = df_out['twilight sparkle'] + df_out['applejack'] + df_out['rarity'] + df_out['pinkie pie'] + df_out['rainbow dash'] + df_out['fluttershy']

    df_out.drop(df_out[df_out.sum_of_words < 5].index, inplace=True)

    # df_out.to_csv('word_list_clean_dialog.csv',index=False)

    out = {}                                                            #this dictionary will only contain words that appear > 5 across ALL speech acts
    for pony in ponies:
        try:
            filtered_df = df_out[["words", pony]]
            df_dict = dict(zip(filtered_df['words'], filtered_df[pony]))
            out[pony] = df_dict
        except:
            out[pony] = {}

    #getting the current working directory
    tgt_path = pathlib.Path.cwd()

    #retrieving the path pointed in -o argument, and splitting the filename and directory name
    output_argument = tgt_path.joinpath(args.output)
    output_fname = output_argument.name
    output_dirname = output_argument.parent

    #creating a directory if it does not exist
    if not output_dirname.exists():
        output_dirname.mkdir()


    with open(args.output,'w+') as outfile:
        json.dump(out,outfile,indent=2)

if __name__ == "__main__":
    main()