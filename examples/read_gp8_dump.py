#!/usr/bin/env python3

''' Slight hack to import from the parent directory '''
import sys
sys.path.append('..')
from RolandGp8 import RolandGp8



def read_sysex(filename):
    ''' Each record in a dump equals one instance of RolandGp8.

    There are cooler/better ways to do this read. However, the example below shows
    importing all records from a Gp8 sysex dump -- each record is 59 bytes long.
    '''
    program = []
    try:
        with open(filename, 'rb') as file:
            for index in range(0, 127):
                program.append(RolandGp8(file.read(59)))
    except (FileExistsError, FileNotFoundError):
        exit(' '.join(["Could not open", filename, "for read. Sorry."]))
    return program

program = read_sysex('sysex_to_read.syx')

for p in program:
    print(str(p) + ": ", end='')
    effects = p.effects
    e = []
    for effect in effects:
        if effects[effect]: e.append(effect)
    print(', '.join(e))

