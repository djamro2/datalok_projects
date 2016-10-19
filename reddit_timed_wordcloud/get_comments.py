
# this module can only run on Python 2 on windows 
# however, it is, build to be compatiable with Python 3 on other platforms

import praw

# connect and get comments
r = praw.Reddit(user_agent='Getting Comment Data by /u/datalok_wordcloud')
subreddit = r.get_subreddit('chicubs')
comments = subreddit.get_comments(limit=500, time='week')

# build string list of comments
commentsList = []
for comment in comments:
	commentsList.append(comment.body)

# save to file called comments.txt
with open('comments.txt', 'w') as outfile:
	for item in commentsList:
		outfile.write(str(item) + '\n')
