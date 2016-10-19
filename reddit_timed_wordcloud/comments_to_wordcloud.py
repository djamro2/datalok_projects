
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np

# config stopwords
stopwords = set(STOPWORDS)
stopwords.add("really")

# Read the whole text.
d = path.dirname(__file__)
text = open(path.join(d, 'comments.txt')).read()

# set up mask for Cubs background
# cubs_mask = np.array(Image.open(path.join(d, "cubs_logo_colored.jpg")))

# generate wordcloud and save to file
wc = WordCloud(background_color="white", stopwords=stopwords, max_font_size=50)
wc.generate(text)

# create coloring from image
# image_colors = ImageColorGenerator(cubs_mask)
# wc.recolor(color_func=image_colors)

# save to file
wc.to_file(path.join(d, "comments.png"))
