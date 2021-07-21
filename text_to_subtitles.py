# importing integrated modules
import os
import re
from datetime import datetime, timedelta

# initializing subtitle length in seconds
dursec = 3

# intializing .txt file locared in the same folder as this python script
inputtxt = 'subtitles.txt'
subpath = os.path.join(os.path.dirname(__file__), inputtxt)
subtxt = open(subpath).read()

# splitting paragraphs into list items with regex
par = re.split('\n{2,}', subtxt)

# pulling number of paragraphs in a text doc
npar = len(par)

# initializing starting subtitle and subtitile duration
tdstart = timedelta(hours=0, seconds=-dursec)
tddur = timedelta(seconds=dursec)

# creating a list of timedeltas
tdlist = []
for i in range(npar+1):
    tdstart = tdstart + tddur
    tdlist.append(tdstart)

# combining created list into a string in accordance with .srt formatting
lcomb = []
for i in range(npar):
    lcomb.append(str(i+1) + '\n' + str(tdlist[i]) + ',000 --> ' + str(
        tdlist[i+1]) + ',000' + '\n' + par[i] + '\n')

# converting the list into a string with the delimiter '\n'
srtstring = '\n'.join(lcomb)

# adding '0' to single digit hours
pat = r'^(\d:)'
repl = '0\\1'
srtstring2 = re.sub(pat, repl, srtstring, 0, re.MULTILINE)

# writing the string to a new file
srtout = os.path.join(os.path.dirname(__file__), 'subtitles.srt')
with open(srtout, 'w') as newfile:
    newfile.write(srtstring2)
