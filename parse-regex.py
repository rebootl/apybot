#!/usr/bin/python3
#
# test parser speed
#
# myparser
#

import re

RE=re.compile('^(?:[:](\S+) )?(\S+)(?: (?!:)(.+?))?(?: [:](.+))?$')

def split_recv_msg(line):

    return RE.split(line)


TESTFILE = "output.file.big"

for line in open(TESTFILE, 'r'):

    sline = split_recv_msg(line)

    #print("sline: ", sline)
