
import praw
import time

from posts import Posts
from api_key import api_key_secret

# authenticate and create reddit instance
reddit = praw.Reddit(client_id='AJL4NgyLiyBFPA',
                     client_secret=api_key_secret,
                     user_agent='testscript by /u/donovan28')

posts = Posts()
postCount = 10
f = open('comments.txt', 'a', encoding='utf-8')


postIds = posts.getPostsAndDelete(postCount)
loopNum = 0

while(len(postIds) == postCount):
	print('Running loop #' + str(loopNum))
	for id in postIds:
		submission = reddit.submission(id=id)
		submission.comments.replace_more(limit=None)
		all_comments = submission.comments.list()
		for comment in all_comments:
			f.write(comment.body + '\n')
	postIds = posts.getPostsAndDelete(postCount)
	time.sleep(2)
	loopNum += 1

f.close()
	