import os,sys
import argparse
import pandas as pd
import numpy as np
import pathlib
import json


def count_filter(df,column_name, pony_name):
	df_filter = df.loc[df[column_name].str.fullmatch(pony_name, case=False)]
	return df_filter.shape[0]


def main():
    #parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input')
    parser.add_argument('-o','--output')
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    df['pony'] = df['pony'].str.lower()

    # print(df.head())
    
    #Collecting all names to be dropped in a list called drop_names
    conditions = [
    df['pony'].str.contains(r'\band'),
    df['pony'].str.contains(r'\ball'),
    df['pony'].str.contains(r'\bponies'),
    df['pony'].str.contains(r'\bothers'),
    ]
    drop_df = df[np.logical_or.reduce(conditions)]

    drop_names = drop_df['pony'].unique().tolist()

    # print(drop_names)
 
    
    all_names = df['pony'].value_counts().index.tolist()    #storing names of all ponies of dataframe
    # print(len(all_names))

    top_chars = {}                                          #dictionary with name of top character as key and no. of speech acts by them as value
    for name in all_names:                                  
        if(name in drop_names):
            pass
        elif(len((top_chars.keys()))>=101):                   
            break
        else:
            count = count_filter(df,'pony',name)
            top_chars[name] = count

    # print(top_chars)
    # print(len(top_chars.keys()))

    top_names = list(top_chars.keys())
    # print(top_names)
    # print(len(top_names))

    task_1 = {}
    for name in top_names:
        task_1[name] = {}

    i = 0
    while (i in df.index):
        try:
            # print("Inside for loop")
            # print(f'index= {i}')
            valid = True
            try:
                curr_pony = df['pony'][i]
                nex_pony = df['pony'][i+1]
                # print(f'current pony= {curr_pony}')
                # print(f'next pony= {nex_pony}')
            except:
                break

            if((curr_pony in drop_names) or (nex_pony in drop_names) or (curr_pony not in top_names) or (nex_pony not in top_names)):
                # print("***This interaction to be nulled***")
                valid = False
                i += 1

            if(curr_pony == nex_pony):
                # print(f"***Skipping this line and next***")
                valid = False
                i += 1                                          #change this to i += 2 if we don't consider second and third pony

            if((df['title'][i] != df['title'][i+1]) or (i == df['title'].iloc[-1])):
                # print("***Episode boundary reached***")
                valid = False
                i += 1

            if(valid == True):
                # print("--TO BE COUNTED--")
                if(nex_pony in task_1[curr_pony].keys() and curr_pony in task_1.keys()):
                    task_1[curr_pony][nex_pony] += 1
                    task_1[nex_pony][curr_pony] += 1
                else:
                    task_1[curr_pony][nex_pony] = 1
                    task_1[nex_pony][curr_pony] = 1
                i += 1
            # print("\n")
        except:
            break
    

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
        json.dump(task_1,outfile,indent=2)     
        

    
    
if __name__ == '__main__':
    main()