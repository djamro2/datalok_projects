
import praw
from datetime import datetime
start = datetime.now()

replace_limit = 800
submission_id = '58jckt'
game_number = 5

# print out start time
print('Starting at', start.strftime('%c'))

# connect and get comments
r = praw.Reddit(user_agent='Getting Comment Data by /u/datalok_wordcloud')
submission = r.get_submission(submission_id=submission_id)
submission.replace_more_comments(limit=replace_limit, threshold=1)
comments = praw.helpers.flatten_tree(submission.comments)

print('Number of comments: ' + str(len(comments)))
print('Time to run: ', datetime.now() - start, 'for a replace limit of', replace_limit)

# save to file called comments.txt
with open('comments_gdt_' + str(game_number) + '.txt', 'w', encoding='utf-8') as outfile:
	for comment in comments:
		outfile.write(str(comment) + '\n')
