
search_words = ['fuck', 'fucking', 'fucked', 'shit', 'bitch', 'dick', 'whore', 'cunt', 'twat', 'ump']

games = [1, 2, 3, 4, 5]
number_of_words = 0

for game in games:
	search_result = {}

	# open comments and build the dictionary
	with open("comments_gdt_" + str(game) + ".txt", "r", encoding="utf-8") as comments:
		all_comments = comments.read().lower()
		number_of_words = len(all_comments.split())
		for word in search_words:
			occurrences = all_comments.count(word)
			search_result[word] = occurrences

	# write output of occurences
	with open("occurrences_gdt_" + str(game) + ".txt", "w", encoding="utf-8") as outfile:
		for word in search_words:
			outstring = word + ": " + str(search_result[word]) + "\n"
			outfile.write(outstring)

	# write output of proportions
	with open("proportions_gdt_" + str(game) + ".txt", "w", encoding="utf-8") as outfile:
		outfile.write('Number of words: ' + str(number_of_words) + "\n")
		for word in search_words:
			proportion = search_result[word] / float(number_of_words)
			percentage = str(round(proportion * 100, 4)) + "%"
			outstring = word + ": " + percentage + "\n"
			outfile.write(outstring)