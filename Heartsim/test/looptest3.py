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

for index, heart in enumerate(hearts):
    print heart, heartlengths[index]
    for index, beats in enumerate(heart):
        print heart[index]

for frame in xrange(frames):
    for index, heart in enumerate(hearts):
        print heart(frame % heartlengths[index]),
    print
