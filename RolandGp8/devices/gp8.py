#!/usr/bin/env python3

''' GP-8 Specific Values Go here. Goal: Mapping the GP-16 should follow the exact same model '''

'''Effects switches are bitwise in two banks'''
BANK_1_EFFECTS_MSB = {
    'PHASER': 0x01,
    'EQUALIZER': 0x02,
    'DELAY': 0x04,
    'CHORUS': 0x08,
}
BANK_2_EFFECTS_LSB = {
    'DYNAMIC_FILTER': 0x01,
    'COMPRESSOR': 0x02,
    'OVERDRIVE': 0x04,
    'DISTORTION': 0x08,
}

''' 
Dictionary describes each byte of the sysex data -- type, range, default, etc... 
Type "flag" is always a hex string. Type "int" is always provided as an int, and
we trust the object to translate it properly (just like when getting an int value)

Default is always provided as a bytes object.

Range is checked on write. It shouldn't be possible to write a value out of range 
into any position. 
'''
data = {
    'SYSEX_BEGIN': {
        'position': 0,
        'length': 1,
        'type': 'flag',
        'category': 'system',
        'name': 'Sysex Begin Message',
        'description': "Sysex first byte.",
        'default': bytes().fromhex('F0'),
        'range': ['F0'],
    },

    'MANUFACTURER_ID': {
        'position': 1,
        'length': 1,
        'type': 'flag',
        'category': 'system',
        'name': 'Manufacturer ID',
        'description': "Unique manufacturer ID",
        'default': bytes().fromhex('41'),
        'range': ['41'],
    },
    
    'DEVICE_ID': {
        'position': 2,
        'length': 1,
        'type': 'flag',
        'category': 'system',
        'name': "Device ID",
        'description': "",
        'default': bytes().fromhex('00'),
        'range': range(16),
    },
    
    'MODEL_ID': {
        'position': 3,
        'length': 1,
        'type': 'flag',
        'category': 'system',
        'name': "Model ID",
        'description': "",
        'default': bytes().fromhex('13'),
        'range': ['13'],
    },
    
    'COMMAND': {
        'position': 4,
        'length': 1,
        'type': 'flag',
        'category': 'system',
        'name': "Command",
        'description': "",
        'default': bytes().fromhex('12'),
        'range': ['12'],
    },
    
    'PROGRAM': {
        'position': 5,
        'length': 1,
        'type': 'bitwise',
        'category': 'meta',
        'name': "Program",
        'description': "",
        'default': 0x00,
        'range': range(64),
    },
    
    'BANK': {
        'position': 5,
        'length': 1,
        'type': 'bitwise',
        'category': 'meta',
        'name': "Bank",
        'description': "",
        'default': 0,
        'range': range(64),
    },
    
    'GROUP': {
        'position': 6,
        'length': 1,
        'type': 'bitwise',
        'category': 'meta',
        'name': "GROUP",
        'description': "",
        'default': 'A',
        'range': [0x0, 0x40],
    },

    'EFFECT_MSB': {
        'position': 7,
        'length': 1,
        'type': 'bitwise',
        'category': 'Effects',
        'name': "Effect MSB",
        'description': "",
        'default': bytes().fromhex('00'),
        'range': range(16),
    },
    
    'EFFECT_LSB': {
        'position': 8,
        'length': 1,
        'type': 'bitwise',
        'category': 'Effects',
        'name': "Effect LSB",
        'description': "",
        'default': bytes().fromhex('00'),
        'range': range(16),
    },  # 00h-0Fh

    #'''Dynamic Filter'''
    'FILTER_SENS': {
        'position': 9,
        'length': 1,
        'type': 'int',
        'category': 'Filter',
        'name': "Sensitivity",
        'description': "",
        'default': 0,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'FILTER_CUTOFF_FREQ': {
        'position': 10,
        'length': 1,
        'type': 'int',
        'category': 'Filter',
        'name': "Cutoff Frequency",
        'description': "",
        'default': 80,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'FILTER_Q': {
        'position': 11,
        'length': 1,
        'type': 'int',
        'category': 'Filter',
        'name': "Quotient",
        'description': "",
        'default': 100,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'FILTER_UP_DOWN': {
        'position': 12,
        'length': 1,
        'type': 'bool',
        'category': 'Filter',
        'name': "Direction",
        'description': "",
        'default': True,
        'range': [True, False],
    },  # 00h = Low Cut, 64h = high cut (0,100)

    # '''Compressor'''
    'COMP_ATTACK': {
        'position': 13,
        'length': 1,
        'type': 'int',
        'category': 'Compressor',
        'name': "Attack",
        'description': "",
        'default': 100,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'COMP_SUSTAIN': {
        'position': 14,
        'length': 1,
        'type': 'int',
        'category': 'Compressor',
        'name': "Sustain",
        'description': "",
        'default': 100,
        'range': range(101),
    },  # 00h-64h (0-100)

    #'''Turbo Overdrive'''
    'OD_TONE': {
        'position': 15,
        'length': 1,
        'type': 'int',
        'category': 'Overdrive',
        'name': "Tone",
        'description': "",
        'default': 60,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'OD_DRIVE': {
        'position': 16,
        'length': 1,
        'type': 'int',
        'category': 'Overdrive',
        'name': "Drive",
        'description': "",
        'default': 0,
        'range': range(101),
    },  # 00h-64h (0-100)

    'OD_TURBO': {
        'position': 17,
        'length': 1,
        'type': 'bool',
        'category': 'Overdrive',
        'name': "Turbo",
        'description': "",
        'default': True,
        'range': [True, False],
    },  # 00h = Off, 64h = On (0,100)

    # '''Distortion'''
    'DIST_TONE': {
        'position': 18,
        'length': 1,
        'type': 'int',
        'category': 'Distortion',
        'name': "Tone",
        'description': "",
        'default': 50,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'DIST_DIST': {
        'position': 19,
        'length': 1,
        'type': 'int',
        'category': 'Distortion',
        'name': "Distortion",
        'description': "",
        'default': 33,
        'range': range(101),
    },  # 00h-64h (0-100)

    # '''Phaser'''
    'PHASER_RATE': {
        'position': 20,
        'length': 1,
        'type': 'int',
        'category': 'Phaser',
        'name': "Rate",
        'description': "",
        'default': 30,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'PHASER_DEPTH': {
        'position': 21,
        'length': 1,
        'type': 'int',
        'category': 'Phaser',
        'name': "Depth",
        'description': "",
        'default': 0,
        'range': range(101),
    },  # 00h-64h (0-100)

    'PHASER_RESONANCE': {
        'position': 22,
        'length': 1,
        'type': 'int',
        'category': 'Phaser',
        'name': "Resonance",
        'description': "",
        'default': 50,
        'range': range(101),
    },  # 00h-64h (0-100)

    # '''Equalizer'''
    'EQ_HI': {
        'position': 23,
        'length': 1,
        'type': 'int',
        'category': 'Equalizer',
        'name': "High",
        'description': "",
        'default': 50,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'EQ_MID': {
        'position': 24,
        'length': 1,
        'type': 'int',
        'category': 'Equalizer',
        'name': "Mid",
        'description': "",
        'default': 50,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'EQ_LO': {
        'position': 25,
        'length': 1,
        'type': 'int',
        'category': 'Equalizer',
        'name': "Low",
        'description': "",
        'default': 60,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'EQ_GAIN': {
        'position': 26,
        'length': 1,
        'type': 'int',
        'category': 'Equalizer',
        'name': "Gain",
        'description': "",
        'default': 50,
        'range': range(101),
    },  # 00h-64h (0-100)

    # '''Delay'''
    'DELAY_LEVEL': {
        'position': 27,
        'length': 1,
        'type': 'int',
        'category': 'Delay',
        'name': "Level",
        'description': "",
        'default': 50,
        'range': range(101),
    },  # 00h-64h (0-100)

    # TODO: Need to deal with these two bytes combined to yeild an int [0-1000]
    'DELAY_TIME': {
        'position': 28,
        'length': 2,
        'type': 'long',
        'category': 'Delay',
        'name': "Time",
        'description': "",
        'default': bytes().fromhex('00'),
        'range': range(1001),
    },  # (0-1000)

    'DELAY_FEEDBACK': {
        'position': 30,
        'length': 1,
        'type': 'int',
        'category': 'Delay',
        'name': "Feedback",
        'description': "",
        'default': 25,
        'range': range(101),
    },  # 00h-64h (0-100)

    # '''Chorus'''
    'CHORUS_RATE': {
        'position': 31,
        'length': 1,
        'type': 'int',
        'category': 'Chorus',
        'name': "Rate",
        'description': "",
        'default': 26,
        'range': range(101),
    },  # 00h-64h (0-100)

    'CHORUS_DEPTH': {
        'position': 32,
        'length': 1,
        'type': 'int',
        'category': 'Chorus',
        'name': "Depth",
        'description': "",
        'default': 15,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'CHORUS_LEVEL': {
        'position': 33,
        'length': 1,
        'type': 'int',
        'category': 'Chorus',
        'name': "Level",
        'description': "",
        'default': 100,
        'range': range(101),
    },  # 00h-64h (0-100)
    
    'CHORUS_PRE_DELAY': {
        'position': 34,
        'length': 1,
        'type': 'int',
        'category': 'Chorus',
        'name': "Pre Delay",
        'description': "",
        'default': 0x41,
        'range': range(101),
    },   # 00h-64h (0-100)
    
    'CHORUS_FEEDBACK': {
        'position': 35,
        'length': 1,
        'type': 'int',
        'category': 'Chorus',
        'name': "Feedback",
        'description': "",
        'default': 27,
        'range': range(101),
    },  # 00h-64h (0-100)

    # '''Misc'''
    'VOLUME': {
        'position': 36,
        'length': 1,
        'type': 'int',
        'category': 'meta',
        'name': "Volume",
        'description': "",
        'default': 20,
        'range': range(101),
    },  # 00h-64h (0-100)

    'EV5_PARAM': {
        'position': 37,
        'length': 1,
        'type': 'int',
        'category': 'meta',
        'name': "EV-5 Parameter",
        'description': "",
        'default': 0,
        'range': range(28),
    },  # 00h-1Bh (0-27, 0=Off, 1= FILTER_SENS...27=MASTER_VOLUME)

    'EXT_CONTROL_1': {
        'position': 38,
        'length': 1,
        'type': 'bool',
        'category': 'meta',
        'name': "External Control 1",
        'description': "",
        'default': False,
        'range': [True, False],
    },  # 00h = Off, 64h = On (0,100)
    
    'EXT_CONTROL_2': {
        'position': 39,
        'length': 1,
        'type': 'bool',
        'category': 'meta',
        'name': "External Control 2",
        'description': "",
        'default': 0,
        'range': [True, False],
    },  # 00h = Off, 64h = On (0,100)

    # '''Name'''
    'NAME': {
        'position': 40,
        'length': 16,
        'type': 'string',
        'name': "Name",
        'description': "",
        'default': '*Untitled       ',
        'range': None
    },  # 20h-7Fh (32-127, 7 bit ASCII)

    'NAME_TERM': {
        'position': 56,
        'length': 1,
        'type': 'flag',
        'name': "String Terminator",
        'description': "",
        'default': bytes().fromhex('00'),
        'range': ['00'],
    },  # 00h (Null)

    #'''Close Packet'''
    'CHECKSUM': {
        'position': 57,
        'length': 1,
        'type': 'flag',
        'name': "Checksum",
        'description': "",
        'default': bytes().fromhex('00'),
        'range': range(128),
    },  # Sum of element 5-56

    'SYSEX_END': {
        'position': 58,
        'length': 1,
        'type': 'flag',
        'name': "Sysex Message End",
        'description': "",
        'default': bytes().fromhex('f7'),
        'range': ['F7'],
    }   # F7
}

'''
Effect MSB/LSB only uses lesser half of the byte, i.e 00-0F
This is handled bitwise. 

Effect on/off MSB
bit 0 -> int(1) -> Phaser
bit 1 -> int(2) -> Eq
bit 2 -> int(4) -> Delay
bit 3 -> int(8) -> Chorus

Effect on/off LSB
bit 0 -> int(1) -> Dynamic Filter
bit 1 -> int(2) -> Compressor
bit 2 -> int(4) -> Overdrive
bit 3 -> int(8) -> Distortion

'''
