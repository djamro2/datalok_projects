
from pylab import *
from collections import OrderedDict

# get the input data
gdt_data_file = open('occurrences_gdt_1.txt', 'r', encoding='utf-8')
gdt_data = gdt_data_file.readlines()

# build the occurrences dict
occurrences = OrderedDict()
for line in gdt_data:
	word = line.split(':')[0]
	count = line.split(':')[1]
	occurrences[word] = count

# create bar length and corresponding y val
val = [int(occurrences[key]) for key in occurrences.keys()]
val += [0] # spacing
val.reverse()
pos = (arange(len(val)) / 2) + .25

# create labels for y-axis
ylabels = ()
for key in occurrences.keys():
	ylabels = ylabels + (key,)
ylabels += (' ', ) # spacing
ylabels = tuple(reversed(ylabels))

# draw the graph itself
barh(pos, val, align='center', height=0.5)
yticks(pos, ylabels)
xlabel('Occurrences')
title('Occurrences of Curse Words in GDT Threads')
# grid(True)

# output barchart and close input
savefig('barchart.png')
gdt_data_file.close()