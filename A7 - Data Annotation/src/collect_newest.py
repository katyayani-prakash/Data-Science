
CLIENT_ID = 'cKnDjN6CLqV41NX0wHNG-Q'
SECRET_KEY = 'VplXPpwA80PXRZuu-y_Q7thM9a6sBw'

import requests
import json
import os,sys
import argparse
import pathlib

def collect_posts(subreddit):
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID,SECRET_KEY)

    data = {
        'grant_type' : 'password',
        'username' : 'temp_id_comp598',
        'password' : '$ungl@ss3s'
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)

    TOKEN = res.json()['access_token']

    headers['Authorization'] = f'bearer {TOKEN}'
    base_url = 'https://oauth.reddit.com'

    res = requests.get(base_url+f'{subreddit}/new', headers=headers, params={'limit':'100'})
    posts=res.json()['data']['children']
    return posts   


def main():
    #parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--output')
    parser.add_argument('-s','--subreddit')
    args = parser.parse_args()
    
    subreddit = args.subreddit

    #calling method to collect posts from the specified subreddit
    posts = collect_posts(subreddit)

    #getting the current working directory
    tgt_path = pathlib.Path.cwd()

    #retrieving the path pointed in -o argument, and splitting the filename and directory name
    output_argument = tgt_path.joinpath(args.output)
    output_fname = output_argument.name
    output_dirname = output_argument.parent

    #creating a directory if it does not exist
    if not output_dirname.exists():
        output_dirname.mkdir()

    #writing posts to the specified file name
    with open(args.output, 'w+') as fp:  
        for post in posts:
            json.dump(post, fp)
            fp.write("\n")
    

if __name__ == "__main__":
    main()
