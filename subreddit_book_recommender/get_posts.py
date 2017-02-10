
import praw
from api_key import api_key_secret

subreddit_tag = 'webdev'
start_time = 1486085981
end_time = 1486690843

# authenticate and create reddit instance
reddit = praw.Reddit(client_id='AJL4NgyLiyBFPA',
                     client_secret=api_key_secret,
                     user_agent='testscript by /u/donovan28')

# subreddit instance
subreddit = reddit.subreddit(subreddit_tag)

# parse through each submission, write to file
i = 0
output = open('posts.txt', 'w', encoding='utf-8')
for submission in subreddit.submissions(start_time, end_time):
	output.write(submission.id + ': ' + submission.title + '\n\n')

output.close()