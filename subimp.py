#!/usr/bin/env python

# importing pandas and re for regular expressions
import pandas as pd
import re

# initializing subtitle length in seconds
sublength = "5s"

# initializing input txt file
tinp = open('subtitles.txt')
tinp = tinp.read()

# splitting paragraphs into list items with regex
par = re.split('\n{2,}', tinp)

# pulling number of paragraphs in a text doc
npar = len(par)

# setting starting and ending timecode
tcstart = pd.timedelta_range(start='0s', periods=npar, freq = sublength)
tcend = pd.timedelta_range(start = sublength, periods=npar, freq = sublength)

# combining created lists into one with .srt formatting
lcomb = []
for i in range(npar):
    lcomb.append(str(i+1) + '\n' + str(tcstart[i]) + ',000 --> ' + str(tcend[i]) + ',000' + '\n' + par[i] + '\n')

# initializing delimiter 
delim = "\n"
# converting list into a string with the delimiter
sub = delim.join(lcomb)

# initializing regex pattern that matches the number of days like '0 days'
spat = '\d* days '
# removing '0 days' from the string
sub1 = re.sub(spat, '', sub)

# writing the string to file
tout = open('subtitles.srt', 'w')
tout.write(sub1)