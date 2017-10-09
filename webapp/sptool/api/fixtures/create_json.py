### Creates a JSON file from text data
###
### NOTICE needs data to have "_" instead of " "
### so that it does not detect different words
### Replace it afterwards

import sys
import os
import json

if len(sys.argv)!=3:
    sys.exit("Input and Output folder needed")

infile = sys.argv[1]
outfile = sys.argv[2]

data = {}
fields = {}

with open(infile, 'r') as infile:
    with open(outfile, 'w') as outfile:
        outfile.write('[')
        for line in infile:
            if (line == "\n"):
                data = {}
                fields = {}
                pk = 1
                data['model'] = next(infile).rstrip()
                data['fields'] = fields
                entries = next(infile).split(" ")
            else:
                data['pk'] = pk
                pk += 1
                words = line.split(" ")
                for ii in range(len(entries)):
                    fields[entries[ii].rstrip()] = words[ii].rstrip()
                json.dump(data, outfile)
                outfile.write(',\n')
        outfile.seek(-2,os.SEEK_END)
        outfile.truncate()
        outfile.write(']')
