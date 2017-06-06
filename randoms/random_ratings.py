# This was just used to see what we'd get
import random
with open ('testestest.txt','w'):
    pass
with open ('test20.txt') as f:
    for line in f:
        split_line = line.split(" ")
        print(split_line)
        if split_line[2] == '0\n' or '0':
            split_line[2] = str(random.randint(1,5))
        with open ('testestest.txt','a') as fo:
            fo.write(str(split_line[0])+' ' +str(split_line[1])+' '+ str(split_line[2])+'\n')
# This will write the stuff from the temp file to the ending file
with open ('test20.txt', 'w'): # Wipes the result file
    pass
# This loop will write everything from the temp file to the result file
with open ('testestest.txt') as f:
    for line in f:
        split_line = line.split(" ")
        print(split_line)
        if split_line[2] == '0\n' or '0':
            split_line[2] = str(random.randint(1,5))
        with open ('test20.txt','a') as fo: # This is where we write to the result file
            fo.write(str(split_line[0])+' ' +str(split_line[1])+' '+ str(split_line[2])+'\n')
