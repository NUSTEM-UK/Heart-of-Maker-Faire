"""First animation attempt, using Python / OPC / FadeCandy.

Let's light this sucker up.
"""

import opc

ADDRESS = "localhost:7890"
# Create a client object
client = opc.Client(ADDRESS)

# Test if it can connect (optional)
if client.can_connect():
    print 'connected to %s' % ADDRESS
else:
    # We could exit here, but instead let's just print a warning
    # and then keep trying to send pixels in case the server
    # appears later
    print 'WARNING: could not connect to %s' % ADDRESS

# Send pixels forever at 30 frames per second
while True:
    my_pixels = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    if client.put_pixels(my_pixels, channel=0):
        print '...'
    else:
        print 'not connected'
    time.sleep(1/30.0)

maxframes = 500
heart01 = [0, 1, 2, 3, 4, 5]
heart02 = [6, 7, 8, 9]
hearts = [heart01, heart02, heart01]
print "Number of hearts:", len(hearts)

heartlengths = []
for i in range(len(hearts)):
    heartlengths.append(len(hearts[i]))

for index, heartlength in enumerate(heartlengths):
    print "Number of frames in heartbeat ", index, " : ", heartlength

print "-------------"

framecount = 0
for framecount in range(maxframes):
    print framecount,
    for i in range(len(hearts)):
        print hearts[i][framecount % len(hearts[i])],
        # On the face of it, the following is fractionally slower. Huh.
        # print hearts[i][framecount % heartlengths[i]],
    # New line, please!
    print
