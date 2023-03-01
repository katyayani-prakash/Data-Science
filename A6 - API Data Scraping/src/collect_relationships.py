import os, sys
import bs4
import argparse
import json
import requests
import pathlib
import re

def save_html(content, filename):
    with open(filename, 'wb') as f:
        f.write(content)


def download_cache(path, person_name):
    print("Scraping the site\n")
    base_url = 'https://www.whosdatedwho.com/dating/'
    completeName = os.path.join(path, person_name)
    #print(completeName)
    c = requests.get(f'{base_url}{person_name}').content
    save_html(c,completeName)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--config_file')
    parser.add_argument('-o','--output')
    args = parser.parse_args()

    #Opening the config file and loading it in a json object
    with open(args.config_file,'r') as infile:
        config_file = json.load(infile)

    #Creating the cache directory, or returning error if it already exists
    cache_dir = config_file['cache_dir']
    try:
        pathlib.Path(cache_dir).mkdir(exist_ok=False)
        print("Creating directory")
    except FileExistsError:
        print("Directory already exists")

    out = {}
    for people in config_file['target_people']:
        completeName = os.path.join(cache_dir, people)
        if(os.path.isfile(completeName)):
            print("File Already Exists")
        else:
            print("File does not exist, creating it")
            download_cache(cache_dir,people)


        soup=bs4.BeautifulSoup(open(completeName, 'rb'), 'html.parser')
        list = []
        rel_list = soup.find("div",{"id": "ff-dating-history-list"})
        if(rel_list == None):
            pass
        else:
            for link in rel_list.find_all('a',attrs={'data-ff-gx':re.compile(r'^View Person')}):
                list.append(link.getText())
                while '' in list:
                    list.remove('')            
        out.update({people:list})

    # print(out)
    with open(args.output,'w+') as outfile:
        json.dump(out,outfile,indent=4)


if __name__ == "__main__":
    main()