# importing pandas and re for regular expressions
# import pandas as pd
import os
import re
from datetime import datetime, timedelta

# initializing subtitle length in seconds
dursec = 5

# intializing .txt file
txt1 = 'subtitles.txt'
subpath = os.path.join(os.path.dirname(__file__), txt1)
subtxt = open(subpath).read()

# splitting paragraphs into list items with regex
par = re.split('\n{2,}', subtxt)

# pulling number of paragraphs in a text doc
npar = len(par)

# initializing starting subtitle and subtitile duration
td2 = timedelta(seconds=dursec)
td1 = timedelta(hours=0, seconds=-dursec)

# creating a list of timedeltas
tdlist = []
for i in range(npar+1):
    td1 = td1 + td2
    tdlist.append(td1)

# combining created list into a string with .srt formatting
lcomb = []
for i in range(npar):
    lcomb.append(str(i+1) + '\n' + str(tdlist[i]) + ',000 --> ' + str(
        tdlist[i+1]) + ',000' + '\n' + par[i] + '\n')

# converting list into a string with the delimiter '\n'
srtstring = '\n'.join(lcomb)

# adding '0' to single digit hours
pat = r'^(\d:)'
repl = '0\\1'
srtstring2 = re.sub(pat, repl, srtstring, 0, re.MULTILINE)

# writing the string to file
srtout = os.path.join(os.path.dirname(__file__), 'subtitles.srt')
with open(srtout, 'w') as newfile:
    newfile.write(srtstring2)
