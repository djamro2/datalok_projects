
from pprint import pprint
import json

f = open('out/webdev_comments.json', 'r', encoding='latin-1')
books_output = open('amazon_books.json', 'w', encoding='latin-1')
posts = json.loads(f.read())
books = {}
comments = []

# build a list of comments to make things easier
for postId in posts.keys():
	comments.extend(posts[postId]['comments'])
print('Number of comments:', len(comments))

for comment in comments:
	if 'amazon.com' not in comment and 'amazon.co.uk' not in comment:
		continue
	for word in comment.split():
		if '/dp/' in word:
			s = word.index('/dp/') + 4
			e = s + 10
			if word[s:e] not in books.keys():
				books[word[s:e]] = {}
				books[word[s:e]]['count'] = 1
				books[word[s:e]]['comments'] = [comment]
			else:
				books[word[s:e]]['count'] += 1
				books[word[s:e]]['comments'].append(comment)

json.dump(books, books_output)

# close files
books_output.close()
f.close()
