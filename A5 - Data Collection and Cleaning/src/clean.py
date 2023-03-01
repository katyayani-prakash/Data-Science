import json
import os, sys
import os.path as osp
from datetime import datetime, timezone
import pytz
import argparse

def isValidJson(string):
    try:
        record = json.loads(string)
        return record
    except:
        return None

def validate_title(record):
    if (record == None):
        return None
    elif("title_text" in record):
        record['title'] = record.pop('title_text')
        return record
    elif("title" in record):
        return record
    else:
        return None

def validate_author(record):
    if(record == None):
        return None
    elif('author' not in record):
    	return record
    elif(((record['author']) == None) or(record['author'] == "") or (record['author'] == "N/A")):
        return None
    else:
        return record

def validate_count(record):
    if(record == None):
        return None
    elif('total_count' in record):
    	if (type(record['total_count'])== int) or (type(record['total_count'])== float) or (type(record['total_count'])== str):
	        try:
	            record['total_count'] = int(record['total_count'])
	        except:
	            return None
    return record

def validate_date(record):
    if(record == None):
        return None
    elif('createdAt' in record):
        try:
            record['createdAt'] = datetime.strptime(record['createdAt'], "%Y-%m-%dT%H:%M:%S%z")
            record['createdAt'] = record['createdAt'].astimezone(pytz.utc)
            record['createdAt'] = datetime.strftime(record['createdAt'],"%Y-%m-%dT%H:%M:%S%z")
            return record
        except:
            return None
    else:
        return record

def validate_tags(record):
    if(record == None):
        return None
    elif('tags' in record):
        join_string = ' '.join(record['tags'])
        new_tags = join_string.split(' ')
        record['tags'] = new_tags
        return record
    else:
        return record


def main():

	#retrieving the paths of clean.py and input json file (example.json)
	script_dir = osp.dirname(__file__)
	data_path = osp.join(script_dir,'..','data')

	#parsing command-line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input')
	parser.add_argument('-o','--output')
	args = parser.parse_args()
	

	#Opening the input file to read it line-by-line
	input_filename = (args.input)
	infile = open(input_filename,'r')
	lines = infile.readlines()

	final = []
	for line in lines:
		a = isValidJson(line)
		b = validate_title(a)
		c = validate_author(b)
		d = validate_date(c)
		e = validate_count(d)
		f = validate_tags(e)
		final.append(f)

	final = list(filter(None, final))

	#Opening output file to write into it
	output_filename = (args.output)
	with open(output_filename,'w+') as outfile:
		for item in final:
			json.dump(item,outfile)
			outfile.write('\n')
		



if __name__ == "__main__":
    main()