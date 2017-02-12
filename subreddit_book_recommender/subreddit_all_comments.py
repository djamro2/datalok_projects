
import os
import os.path as path
import calendar
import json
import time
import math

def findTotalLoopsRequired(startTime, endTime, num_days_per_loop):
	diff = endTime - startTime
	return math.ceil(diff / getDaysInSeconds(num_days_per_loop))

def addComments(reddit, posts, output, filename):
	"""
	Go through each postId in the posts and get an array of comments
	for this post.
	"""

	print('\n Now adding comments to ' + filename)
	num_posts = len(posts.keys())

	for idx, postId in enumerate(posts.keys()):
		print('On post {0} out of {1}.'.format(idx+1, num_posts))
		if (posts[postId]['comments'] and len(posts[postId]['comments']) > 0):
			print('Skipping this post, already done')
			continue

		submission = reddit.submission(id=postId)
		submission.comments.replace_more(limit=None)
		all_comments = submission.comments.list()

		all_comments_text = []
		for comment in all_comments:
			all_comments_text.append(comment.body)
		posts[postId]['comments'] = all_comments_text

		print('Added comments to this post, sleeping now')
		time.sleep(2)

		if (idx > 0 and idx % 5 == 0):
			print('Writing to file')
			writeToFile(posts, output)

	writeToFile(posts, output)

def addPosts(subreddit, startTime, endTime, posts, output, filename, num_days=2):
	"""
	Add all of the posts between the startTime and endTime
	Returns the posts dictionary with all of the posts
	"""

	print('Now adding posts to ' + filename)

	startTimeLoop = getLatestPostEntry(posts, startTime)
	endTimeLoop = min([startTimeLoop + getDaysInSeconds(num_days), endTime])
	loopNum = 1
	total_loops_required = findTotalLoopsRequired(startTimeLoop, endTime, num_days)

	while(startTimeLoop < endTime):
		print('On loop {0} out of {1} in adding posts'.format(loopNum, total_loops_required))
		for submission in subreddit.submissions(startTimeLoop, endTimeLoop):
			posts[submission.id] = {}
			posts[submission.id]['created'] = submission.created
			posts[submission.id]['comments'] = []
		writeToFile(posts, output)
		startTimeLoop = endTimeLoop
		endTimeLoop  = min([endTimeLoop + getDaysInSeconds(num_days), endTime])
		loopNum += 1
		print(endTimeLoop)

		# TEMP
		if (loopNum > 2):
			break

	# return the final posts dict in case this is needed
	return posts


def createFolder(foldername):
	"""
	Will create this folder if it does not exist at the moment
	"""
	if (path.exists(foldername)):
		return
	try:
		os.makedirs(foldername)
	except OSError as err: 
		if err.errno != errno.EEXIST:
			raise

def getDaysInSeconds(days):
	return 60 * 60 * 24 * days

def getFileContent(filename):
	content = None
	if path.exists(filename):
		f = open(filename, 'r', encoding='utf-8')
		content = f.read()
		f.close()
	return content

def getLatestPostEntry(posts, startTime):
	"""
	Will find the latest timestamp given a dictionary of posts
	Ensure that the posts dictionary exists
	"""
	if (posts is None or len(posts.keys()) == 0):
		return None

	latestCreatedTime = startTime
	for postId in posts.keys():
		createdTime = posts[postId]['created']
		if (createdTime > latestCreatedTime):
			latestCreatedTime = createdTime

	return latestCreatedTime

def writeToFile(posts, fp):
	fp.seek(0) # write to beginning
	json.dump(posts, fp)

def scrape(subreddit, startTime, reddit, endTime=None, filename=None, foldername=None, quiet=1):
	"""
	Main scrape function, get all posts first, do so one week at
	a time. At the start of each iteration go from the first one that
	has no comment values, in case the last iteration failed.
	Then go through one post every 2 seconds
	"""

	# set filename if not provided
	if (filename is None):
		filename = subreddit + '_comments'
	filename += '.json'

	# set endTime to current if not provided
	if (endTime is None):
		endTime = calendar.timegm(time.gmtime())

	# set foldername options is exists
	if (foldername):
		filename = foldername + '/' + filename
		createFolder(foldername)

	# get all the post comments if any exist at the moment
	posts_str = getFileContent(filename)
	posts = {}
	if (posts_str is not None and len(posts_str) > 0):
		posts = json.loads(posts_str)

	# out file for writing
	output = None
	if (path.exists(filename)):
		output = open(filename, 'r+', encoding='utf-8') # don't destroy file
	else:
		output = open(filename, 'w', encoding='utf-8')

	# subreddit instance
	subreddit = reddit.subreddit(subreddit)

	# add all of the posts to the file
	addPosts(subreddit, startTime, endTime, posts, output, filename)
	print('Added all posts')

	# add comments now that we've added all possible posts
	addComments(reddit, posts, output, filename)
	print('Added all comments')

	# close the output file
	output.close()




