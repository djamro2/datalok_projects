
import calendar
import praw
import time

from api_key import api_key_secret
from posts import Posts

subreddit_tag = 'webdev'
start_time = calendar.timegm(time.strptime('01/07/2016', '%m/%d/%Y'))
end_time = calendar.timegm(time.strptime('01/14/2016', '%m/%d/%Y'))

# authenticate and create reddit instance
reddit = praw.Reddit(client_id='AJL4NgyLiyBFPA',
                     client_secret=api_key_secret,
                     user_agent='testscript by /u/donovan28')

# subreddit instance
subreddit = reddit.subreddit(subreddit_tag)

# create an instance of Posts, use this to add
posts = Posts()

# parse through each submission, write to file
for submission in subreddit.submissions(start_time, end_time):
	posts.addPost(submission.id)

# write all posts to file
posts.writeToFile()