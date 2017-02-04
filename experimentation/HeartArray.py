import serial
import time
import random
import re

loadSavedData = raw_input("Do you wish to load previous data? y/n ")

if loadSaved == 'y':
    

# get information on the total possible number of heart cells
totalHearts = int(raw_input("What is the total number of heart cells?  "))

# setup the heart rate Arduino serial connection, choose port and baud depending on Arduino and Pi settings
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Create the heartQR map
heartQR = [0] * totalHearts
print("Here's your empty list...")
print(heartQR)
print("")

#Create a list of the empty cells that need to be filled
emptyCells = []
for i in range(0,totalHearts):
    emptyCells.append(i)
print("Here's your remaining empty cells...")
print(emptyCells)
print("")

    
while False:
    if not emptyCells:      #if there are no empty spaces left, end the programme
        break
    status = True
    newQRcode = ser.readline()  #read the current heart rate from the serial    
    codeNum = [int(s) for s in re.findall(r'\d+', newQRcode)] #strip the integers from the string
    print(codeNum[0])
    for i in heartCells:        #check if we already have this code logged
        if codeNum[0] == i:
            print("We've already had this code")
            status = False
            
    if status == True:          #if we've not had this code before randomly assign it to  cell and remove the cell from the empties list
        position = random.choice(emptyCells)
        print("Enter into cell %s:" % position)
        print(codeNum[0])
        emptyCells.remove(position)
        heartCells[position] = codeNum[0]

print("All cells are filled")

print(heartQR)
        
            
            
