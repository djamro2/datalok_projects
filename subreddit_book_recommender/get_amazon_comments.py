
import json

# open the file
f = open('out/webdev_comments.json', 'r', encoding='utf-8')
posts = json.loads(f.read())

output = open('amazon_comments.txt', 'w', encoding='utf-8')

for postId in posts.keys():
	if ('comments' not in posts[postId].keys() or len(posts[postId]['comments']) == 0):
		continue
	for comment in posts[postId]['comments']:
		if 'amazon.com' in comment or 'amazon.co.uk' in comment:
			output.write(comment + '\n')

output.close()
f.close()
