#!/usr/bin/python3
#
# test parser speed
#
# myparser
#

def split_recv_msg(line):
    '''Split received IRC message into defined parts.

Returns: prefix command args text'''

    # opt: use else instead of default value to avoid write
    #prefix = None
    #text = None

    if line[0] == ':':
        prefix, line = line[1:].split(' ', 1)
    else:
        prefix = None

    if line.find(' :') != -1:
        line, text = line.split(' :', 1)
    else:
        text = None

    if line.find(' ') != -1:
        command, line = line.split(' ', 1)
        args = line.split()
    else:
        command = line
        args = None

    return prefix, command, args, text

TESTFILE = "output.file.big"

for line in open(TESTFILE, 'r'):

    sline = split_recv_msg(line)
    #sline = split_recv_msg(line)

    #print("sline: ", sline)
