
import subreddit_all_comments
import calendar
import time
import praw
from api_key import api_key_secret

# start from the beginning of 2016
start_time = '01/01/2016'
start_timestamp = calendar.timegm(time.strptime('01/07/2016', '%m/%d/%Y'))


# authenticate and create reddit instance
reddit = praw.Reddit(client_id='AJL4NgyLiyBFPA',
                     client_secret=api_key_secret,
                     user_agent='testscript by /u/donovan28')

subreddit_all_comments.scrape('webdev', start_timestamp, foldername='out', reddit=reddit)