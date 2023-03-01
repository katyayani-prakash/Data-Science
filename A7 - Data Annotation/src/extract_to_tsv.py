import os,sys
import pandas as pd
import argparse
import json
import pathlib

def main():
    #parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--out_file')
    parser.add_argument('json_file')
    parser.add_argument('num_of_posts',type=int)
    args = parser.parse_args()

    #print(args)

    infile = args.json_file
    outfile = args.out_file
    num_of_posts = args.num_of_posts

    file = open(infile,'r')
    lines = file.readlines()

    # append relevant data to dataframe
    df = pd.DataFrame()

    for line in lines:
        record=json.loads(line)
        df = df.append({
            'Name': record['kind']+'_'+record['data']['id'],
            'title': record['data']['title'],
            'coding':""
        },ignore_index=True)


    #retrieving the path pointed in -o argument, and splitting the filename and directory name
    tgt_path = pathlib.Path.cwd()
    
    output_argument = tgt_path.joinpath(outfile)
    #output_fname = output_argument.name
    output_dirname = output_argument.parent

    #creating a directory if it does not exist
    if not output_dirname.exists():
        output_dirname.mkdir()
        
    try:
        out = df.sample(n=num_of_posts)
        out.to_csv(outfile,index=False,sep='\t')
    except:
        df.to_csv(outfile,index=False,sep='\t')

if __name__ == "__main__":
    main()