# Let's make a list of lists
frames = 50
heart01 = [0, 1, 2, 3, 4, 5]
heart02 = [6, 7, 8, 9]
hearts = [heart01, heart02, heart01]
print "Number of hearts:", len(hearts)

heartlengths = []
for i in range(len(hearts)):
    heartlengths.append(len(hearts[i]))

for index, heartlength in enumerate(heartlengths):
    print "Number of frames in heartbeat ", index, " : ", heartlength

# print heartlengths[0]
# print len(hearts[1])

# Just to prove I can do it, here's a loop using iterators.
# ...but man, this hurts my heard for multidimensional arrays.
# Also: if I have to port this to Processing for performance reasons,
# I can't imagine how grateful I'm going to be to my former self
# for adopting C-style loop idioms over more Pythonic approaches.

# for index, heart in enumerate(hearts):
#     print heart, heartlengths[index]
#     for index, beats in enumerate(heart):
#         print heart[index]

# ...and now here's a sane way of producing the same thing:
for i in range(len(hearts)):
    print "Heart: ", i
    for j in range(len(hearts[i])):
        print hearts[i][j]
