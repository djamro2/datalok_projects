
from PIL import Image

# open the image
picture = Image.open('test_image.jpg')

# get image data
width, height = picture.size
pixels = picture.load()

print(pixels[0, 0])

# create new image pixels array
colors = []
for i in range(width):
	for j in range(height):
		current_color = pixels[j,i]
		new_color = (current_color[0], current_color[1], 0)
		colors.append(new_color)

# provide new pixels and save
picture.putdata(colors)
picture.save('newimage2.png')
