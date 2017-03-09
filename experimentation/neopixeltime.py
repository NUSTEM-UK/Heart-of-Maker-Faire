from timeit import Timer
from time import sleep

t = Timer("""x.index(123)""", setup="""x = range(1000)""")



print (t.timeit())
sleep(1)
print (t.timeit())