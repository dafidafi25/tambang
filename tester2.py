from Enum import GateSetting



lines = []
with open('setting.txt') as f:
    lines = f.readlines()

for line in lines:

    print(line[0:line.index("=")])
   
    print(type( line[line.index("=")+1: len(line)]))