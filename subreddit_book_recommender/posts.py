
from pathlib import Path

fname = 'posts.txt'

class Posts:
	'Helper class to save/use post ids'

	def __init__(self):
		self.posts = self.getAllPosts()

	def addPost(self, postId):
		"""
		Add this postId to the list of posts
		"""
		if postId not in self.posts:
			self.posts.append(postId)

	def getAllPosts(self):
		"""
		returns all the possible posts as a list, or if the 
		file does not exist, then an empty list
		"""
		if (self.postsFileExists()):
			with open(fname) as f:
				content = f.readlines()
				posts = [x.strip() for x in content]
			return posts
		else:
			return []

	def postsFileExists(self):
		""" 
		checks to see if a previous post file was made
		"""
		return Path("posts.txt").is_file()

	def writeToFile(self):
		"""
		Overwrite the previous post file with any changes made 
		to the list of posts
		"""
		with open(fname, 'w') as f:
			for post in posts:
				f.write(post + '\n')