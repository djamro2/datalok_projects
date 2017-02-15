
import json

# open the files
f = open('amazon_comments.txt', 'r', encoding='utf-8')
output = open('amazon_books.json', 'w', encoding='utf-8')
comments = f.read().split()

print('Number of comments:', len(comments))

# close files
comments.close()
f.close()
