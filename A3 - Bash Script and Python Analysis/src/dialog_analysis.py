import argparse
import csv
import sys
import pandas as pd
import re
import json
import math

#parsing the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o')
parser.add_argument('input')
args = parser.parse_args()
#print (args.o)
#print (args.input)


#reading the input file
df = pd.read_csv(args.input)
#print(df.head())

#defining a function to count the number of speech acts 
def count_filter(column_name, pony_name):
	df_filter = df.loc[df[column_name].str.fullmatch(pony_name, case=False)]
	return df_filter.shape[0]


#defining a function to calculate verbosity
#simple fraction function with input taken from count function and total speeach acts
#truncating the fraction to 2 decimal places to match the format shown in assignment handout
def verbosity(num,den):
	frac = num/den
	frac = format(frac, ".2f")
	return frac


#retrieving count of each pony
ts = count_filter('pony','twilight sparkle')
#print(ts)

aj = count_filter('pony','applejack')
#print(aj)

rr = count_filter('pony','rarity')
#print(rr)

pp = count_filter('pony','pinkie pie')
#print(pp)

rd = count_filter('pony','rainbow dash')
#print(rd)

fs = count_filter('pony','fluttershy')
#print(fs)

#retrieving verbosity of each pony
total = df.shape[0]

ts_v = verbosity(ts,total)
#print(ts_v)

aj_v = verbosity(aj,total)
#print(aj_v)

rr_v = verbosity(rr,total)
#print(rr_v)

pp_v = verbosity(pp,total)
#print(pp_v)

rd_v = verbosity(rd,total)
#print(rd_v)

fs_v = verbosity(fs,total)
#print(fs_v)


#writing all these values to a python dictionary and dumping them on the output jason file
out = {}
out['count'] = {}
out['verbosity'] ={}

out = {'count':
	{
		'twilight sparkle' :ts,
                'applejack': aj,
                'rarity': rr,
                'pinkie pie': pp,
                'rainbow dash': rd,
                'fluttershy': fs
	},
	'verbosity':
	{
		'twilight sparkle': ts_v,
                'applejack': aj_v,
                'rarity': rr_v,
                'pinkie pie': pp_v,
                'rainbow dash': rd_v,
                'fluttershy': fs_v
	}
}

with open(args.o,'w') as outfile:
	json.dump(out,outfile,indent=4)


