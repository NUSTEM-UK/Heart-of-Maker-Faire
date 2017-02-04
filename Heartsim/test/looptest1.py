# Let's make a list
heart01 = [0, 1, 2, 3, 4, 5]
print len(heart01)

for i in xrange(50):
    print heart01[i % len(heart01)]
