import praw
import os
import json
from dotenv import load_dotenv
import random


load_dotenv()
REDDIT_APP_ID = 'ev455l_XxV7R5g'
REDDIT_APP_SECRET = 's9Tz42N_AAPe0I0zawhSR7Mbio3TQQ'

reddit= praw.Reddit(client_id=REDDIT_APP_ID, client_secret=REDDIT_APP_SECRET, user_agent="first_python_app_By_anish",username = "JuJuAnish")
#print(reddit.user.me())

def randomMeme(str="memes"):
    subreddit1 = str
    submissions = reddit.subreddit(subreddit1).hot()
    for i in range(0, random.randint(1, 10)):
        submission = next(x for x in submissions if not x.stickied)    
    print(submission.url)
    return submission.url

meme = randomMeme()
#print(meme)