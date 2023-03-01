
CLIENT_ID = 'cKnDjN6CLqV41NX0wHNG-Q'
SECRET_KEY = 'VplXPpwA80PXRZuu-y_Q7thM9a6sBw'

import requests
import json

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
def collect_posts(subreddits):
    all_posts = []
    for subreddit in subreddits:
        res = requests.get(base_url+f'/r/{subreddit}/new',
                          headers=headers,
                          params={'limit':'100'})
        posts=res.json()['data']['children']
        all_posts.append(posts)
    return all_posts   




approach1_subreddits = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
approach1_posts = collect_posts(approach1_subreddits)


with open('sample1.json', 'w+') as fp:      
    for posts in approach1_posts:
        for items in posts:
            json.dump(items, fp)
            fp.write("\n")


approach2_subreddits = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends','unpopularopinion']
approach2_posts = collect_posts(approach2_subreddits)

with open('sample2.json', 'w+') as fp:      
    for posts in approach2_posts:
        for items in posts:
            json.dump(items, fp)
            fp.write("\n")



