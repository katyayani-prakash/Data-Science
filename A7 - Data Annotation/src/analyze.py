import os,sys
import argparse
import json
import pandas as pd
import pathlib

def filter_dataframe(dataframe,filter):
    new_df = dataframe.loc[dataframe['coding'] == filter]
    return new_df

def main():
    #parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input')
    parser.add_argument('-o','--output')
    args = parser.parse_args()


    df = pd.read_csv(args.input,sep='\t')

    course = food = residence = other = 0

    course = len(filter_dataframe(df,'c'))

    food = len(filter_dataframe(df,'f'))

    residence = len(filter_dataframe(df,'r'))

    other = len(filter_dataframe(df,'o'))

    out = {'course-related' : course,
            'food-related' : food,
            'residence-related' : residence,
            'other' : other	
        }

    
    if(args.output):
        #retrieving the path pointed in -o argument, and splitting the filename and directory name
        tgt_path = pathlib.Path.cwd()
        
        output_argument = tgt_path.joinpath(args.output)
        #output_fname = output_argument.name
        output_dirname = output_argument.parent

        #creating a directory if it does not exist
        if not output_dirname.exists():
            output_dirname.mkdir()
        
        #writing posts to the specified file name
        with open(args.output, 'w+') as fp:
                json.dump(out, fp, indent=2)
    
    else:
        str = json.dumps(out,indent=2)
        print(str)



if __name__ == "__main__":
    main()