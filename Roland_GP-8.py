#!/usr/bin/env python3

import binascii
import devices.gp8 as gp8

class RolandGp8():
    ''' Object oriented abstraction for Roland GP-8 ops and storage formats

        Refer to GP-8 Notes.md, and the Roland GP-8 Owner's Manual for deep dives.

    '''
    def __init__(self, record=None):
        ''' If initialized with no params, the object returned is a "blank" record
            with the address set to write to the immediate mode temp area at '00 00' 
        '''
        if record == None:
            record = binascii.unhexlify(b'f041001312000000000050646464643c006432211e003232323c64320310191a0f64411b140000002a556e7469746c656420202020202020200012f7')
        self._record = bytearray(record)
        self._gp8 = gp8.data
        self._effect_lookup = gp8.BANK_1_EFFECTS_MSB
        self._effect_lookup.update(gp8.BANK_2_EFFECTS_LSB)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ''.join([str(self.group), '-', str(self.bank), '-', str(self.program), ':', self.name])

    def csv_hex(self):
        csv = []
        for byte in p._record:
            csv.append(byte.to_bytes(1, 'big').hex())
        return ','.join(csv)

    def _read_value(self, name):
        ''' Read data from the sysex buffer using the data dictionary '''
        data = self._gp8[name]
        if data['type'] in ['int', 'bitwise']:
            return self._record[data['position']]
        if data['type'] == 'bool':
            if self._record[data['position']] == 100:
                return True
            elif self._record[data['position']] == 0:
                return False
            else:
                return False
        if data['type'] == 'flag':
            return self._record[data['position']:data['position'] + data['length']]

    def _write_value(self, name, value):
        ''' Write data from the sysex buffer using the data dictionary '''
        data = self._gp8[name]
        if data['type'] in ['int', 'bitwise'] and type(value) == type(0):
            self._record[data['position']:data['position'] + data['length']] = [value]
        if data['type'] == 'bool':
            if value:
                self._record[data['position']:data['position'] + data['length']] = [100]
            else:
                self._record[data['position']:data['position'] + data['length']] = [0]

    def _effect_set(self, bank, ef, value):
        ''' Read data from the sysex buffer using the data dictionary '''
        if value != bool(self._read_value(bank) & self._effect_lookup[ef] == self._effect_lookup[ef]):
            # XOR flip the bit
            self._write_value(bank, self._read_value(bank) ^ self._effect_lookup[ef])
    
    @property
    def name(self):
        data = self._gp8['NAME']
        return self._record[data['position']:data['position'] + data['length']].decode()

    @name.setter
    def name(self, value):
        data = self._gp8['NAME']
        while len(value) <= data['length']:
            '''Pad the string to length with spaces'''
            value = value + " "
        self._record[data['position']:data['position'] +
                     data['length']] = bytes(value, 'ascii')

    @name.deleter
    def name(self):
        raise NotImplementedError

    @property
    def volume(self):
        return self._read_value('MASTER_VOLUME')

    @volume.setter
    def volume(self, value):
        return self._write_value('MASTER_VOLUME', value)

    @volume.deleter
    def volume(self):
        raise NotImplementedError

    #EFFECT BIT SWITCHES

    #Dynamic Filter
    @property
    def filter(self): 
        return bool(self._read_value('EFFECT_LSB') & self._effect_lookup['DYNAMIC_FILTER'] == self._effect_lookup['DYNAMIC_FILTER'])
    
    @filter.setter
    def filter(self, value):
        self._effect_set('EFFECT_LSB', 'DYNAMIC_FILTER', value)

    @filter.deleter
    def filter(self):
        raise NotImplementedError
    
    #Compressor
    @property
    def compressor(self):
        return bool(self._read_value('EFFECT_LSB') & self._effect_lookup['COMPRESSOR'] == self._effect_lookup['COMPRESSOR'])
    
    @compressor.setter
    def compressor(self, value):
        self._effect_set('EFFECT_LSB', 'COMPRESSOR', value)

    @compressor.deleter
    def compressor(self):
        raise NotImplementedError
    
    #Overdrive
    @property
    def overdrive(self):
        return bool(self._read_value('EFFECT_LSB') & self._effect_lookup['OVERDRIVE'] == self._effect_lookup['OVERDRIVE'])
    
    @overdrive.setter
    def overdrive(self, value):
        self._effect_set('EFFECT_LSB', 'OVERDRIVE', value)

    @overdrive.deleter
    def overdrive(self):
        raise NotImplementedError

    #Distortion
    @property
    def distortion(self):
        return bool(self._read_value('EFFECT_LSB') & self._effect_lookup['DISTORTION'] == self._effect_lookup['DISTORTION'])
      
    @distortion.setter
    def distortion(self, value):
        self._effect_set('EFFECT_LSB', 'DISTORTION', value)

    @distortion.deleter
    def distortion(self):
        raise NotImplementedError

    #Phaser
    @property
    def phaser(self):
        return bool(self._read_value('EFFECT_MSB') & self._effect_lookup['PHASER'] == self._effect_lookup['PHASER'])

    @phaser.setter
    def phaser(self, value):
        self._effect_set('EFFECT_MSB', 'PHASER', value)

    @phaser.deleter
    def phaser(self):
        raise NotImplementedError

    #Equalizer
    @property
    def equalizer(self):
        return bool(self._read_value('EFFECT_MSB') & self._effect_lookup['EQUALIZER'] == self._effect_lookup['EQUALIZER'])
    
    @equalizer.setter
    def equalizer(self, value):
        self._effect_set('EFFECT_MSB', 'EQUALIZER', value)

    @equalizer.deleter
    def equalizer(self):
        raise NotImplementedError

    #Delay
    @property
    def delay(self):
        return bool(self._read_value('EFFECT_MSB') & self._effect_lookup['DELAY'] == self._effect_lookup['DELAY'])
    
    @delay.setter
    def delay(self, value):
        self._effect_set('EFFECT_MSB', 'DELAY', value)

    @delay.deleter
    def delay(self):
        raise NotImplementedError

    #Chorus
    @property
    def chorus(self):
        return bool(self._read_value('EFFECT_MSB') & self._effect_lookup['CHORUS'] == self._effect_lookup['CHORUS'])
    
    @chorus.setter
    def chorus(self, value):
        self._effect_set('EFFECT_MSB', 'CHORUS', value)

    @chorus.deleter
    def chorus(self):
        raise NotImplementedError

    #For convenience
    @property
    def effects(self):
        return {
            'Phaser': self.phaser,
            'Equalizer': self.equalizer,
            'Delay': self.delay,
            'Chorus': self.chorus,
            'Dynamic Filter': self.filter,
            'Compressor': self.compressor,
            'Overdrive': self.overdrive,
            'Distortion': self.distortion,
        }
        
    #
    #Effect Properties
    #
    # FILTER_SENS

    @property
    def filter_sens(self):
        return self._read_value('FILTER_SENS')

    @filter_sens.setter
    def filter_sens(self, value):
        return self._write_value('FILTER_SENS', value)

    @filter_sens.deleter
    def filter_sens(self):
        raise NotImplementedError

    # FILTER_CUTOFF_FREQ
    @property
    def filter_cutoff_freq(self):
        return self._read_value('FILTER_CUTOFF_FREQ')

    @filter_cutoff_freq.setter
    def filter_cutoff_freq(self, value):
        return self._write_value('FILTER_CUTOFF_FREQ', value)

    @filter_cutoff_freq.deleter
    def filter_cutoff_freq(self):
        raise NotImplementedError

    # FILTER_Q
    @property
    def filter_q(self):
        return self._read_value('FILTER_Q')

    @filter_q.setter
    def filter_q(self, value):
        return self._write_value('FILTER_Q', value)

    @filter_q.deleter
    def filter_q(self):
        raise NotImplementedError

    # FILTER_UP_DOWN
    @property
    def filter_up_down(self):
        return self._read_value('FILTER_UP_DOWN')

    @filter_up_down.setter
    def filter_up_down(self, value):
        return self._write_value('FILTER_UP_DOWN', value)

    @filter_up_down.deleter
    def filter_up_down(self):
        raise NotImplementedError

    # COMP_ATTACK
    @property
    def comp_attack(self):
        return self._read_value('COMP_ATTACK')

    @comp_attack.setter
    def comp_attack(self, value):
        return self._write_value('COMP_ATTACK', value)

    @comp_attack.deleter
    def comp_attack(self):
        raise NotImplementedError

    # COMP_SUSTAIN
    @property
    def comp_sustain(self):
        return self._read_value('COMP_SUSTAIN')

    @comp_sustain.setter
    def comp_sustain(self, value):
        return self._write_value('COMP_SUSTAIN', value)

    @comp_sustain.deleter
    def comp_sustain(self):
        raise NotImplementedError

    # OD_TONE
    @property
    def od_tone(self):
        return self._read_value('OD_TONE')

    @od_tone.setter
    def od_tone(self, value):
        return self._write_value('OD_TONE', value)

    @od_tone.deleter
    def od_tone(self):
        raise NotImplementedError

    # OD_DRIVE
    @property
    def od_drive(self):
        return self._read_value('OD_DRIVE')

    @od_drive.setter
    def od_drive(self, value):
        return self._write_value('OD_DRIVE', value)

    @od_drive.deleter
    def od_drive(self):
        raise NotImplementedError

    # OD_TURBO
    @property
    def od_turbo(self):
        return self._read_value('OD_TURBO')

    @od_turbo.setter
    def od_turbo(self, value):
        return self._write_value('OD_TURBO', value)

    @od_turbo.deleter
    def od_turbo(self):
        raise NotImplementedError

    # DIST_TONE
    @property
    def dist_tone(self):
        return self._read_value('DIST_TONE')

    @dist_tone.setter
    def dist_tone(self, value):
        return self._write_value('DIST_TONE', value)

    @dist_tone.deleter
    def dist_tone(self):
        raise NotImplementedError

    # DIST_DIST
    @property
    def dist_dist(self):
        return self._read_value('DIST_DIST')

    @dist_dist.setter
    def dist_dist(self, value):
        return self._write_value('DIST_DIST', value)

    @dist_dist.deleter
    def dist_dist(self):
        raise NotImplementedError

    # PHASER_RATE
    @property
    def phaser_rate(self):
        return self._read_value('PHASER_RATE')

    @phaser_rate.setter
    def phaser_rate(self, value):
        return self._write_value('PHASER_RATE', value)

    @phaser_rate.deleter
    def phaser_rate(self):
        raise NotImplementedError

    # PHASER_DEPTH
    @property
    def phaser_depth(self):
        return self._read_value('PHASER_DEPTH')

    @phaser_depth.setter
    def phaser_depth(self, value):
        return self._write_value('PHASER_DEPTH', value)

    @phaser_depth.deleter
    def phaser_depth(self):
        raise NotImplementedError

    # PHASER_RESONANCE
    @property
    def phaser_resonance(self):
        return self._read_value('PHASER_RESONANCE')

    @phaser_resonance.setter
    def phaser_resonance(self, value):
        return self._write_value('PHASER_RESONANCE', value)

    @phaser_resonance.deleter
    def phaser_resonance(self):
        raise NotImplementedError

    # EQ_HI
    @property
    def eq_hi(self):
        return self._read_value('EQ_HI')

    @eq_hi.setter
    def eq_hi(self, value):
        return self._write_value('EQ_HI', value)

    @eq_hi.deleter
    def eq_hi(self):
        raise NotImplementedError

    # EQ_MID
    @property
    def eq_mid(self):
        return self._read_value('EQ_MID')

    @eq_mid.setter
    def eq_mid(self, value):
        return self._write_value('EQ_MID', value)

    @eq_mid.deleter
    def eq_mid(self):
        raise NotImplementedError

    # EQ_LO
    @property
    def eq_lo(self):
        return self._read_value('EQ_LO')

    @eq_lo.setter
    def eq_lo(self, value):
        return self._write_value('EQ_LO', value)

    @eq_lo.deleter
    def eq_lo(self):
        raise NotImplementedError

    # EQ_GAIN
    @property
    def eq_gain(self):
        return self._read_value('EQ_GAIN')

    @eq_gain.setter
    def eq_gain(self, value):
        return self._write_value('EQ_GAIN', value)

    @eq_gain.deleter
    def eq_gain(self):
        raise NotImplementedError

    # DELAY_LEVEL
    @property
    def delay_level(self):
        return self._read_value('DELAY_LEVEL')

    @delay_level.setter
    def delay_level(self, value):
        return self._write_value('DELAY_LEVEL', value)

    @delay_level.deleter
    def delay_level(self):
        raise NotImplementedError

    # DELAY_FEEDBACK
    @property
    def delay_feedback(self):
        return self._read_value('DELAY_FEEDBACK')

    @delay_feedback.setter
    def delay_feedback(self, value):
        return self._write_value('DELAY_FEEDBACK', value)

    @delay_feedback.deleter
    def delay_feedback(self):
        raise NotImplementedError

    # CHORUS_RATE
    @property
    def chorus_rate(self):
        return self._read_value('CHORUS_RATE')

    @chorus_rate.setter
    def chorus_rate(self, value):
        return self._write_value('CHORUS_RATE', value)

    @chorus_rate.deleter
    def chorus_rate(self):
        raise NotImplementedError

    # CHORUS_DEPTH
    @property
    def chorus_depth(self):
        return self._read_value('CHORUS_DEPTH')

    @chorus_depth.setter
    def chorus_depth(self, value):
        return self._write_value('CHORUS_DEPTH', value)

    @chorus_depth.deleter
    def chorus_depth(self):
        raise NotImplementedError

    # CHORUS_LEVEL
    @property
    def chorus_level(self):
        return self._read_value('CHORUS_LEVEL')

    @chorus_level.setter
    def chorus_level(self, value):
        return self._write_value('CHORUS_LEVEL', value)

    @chorus_level.deleter
    def chorus_level(self):
        raise NotImplementedError

    # CHORUS_PRE_DELAY
    @property
    def chorus_pre_delay(self):
        return self._read_value('CHORUS_PRE_DELAY')

    @chorus_pre_delay.setter
    def chorus_pre_delay(self, value):
        return self._write_value('CHORUS_PRE_DELAY', value)

    @chorus_pre_delay.deleter
    def chorus_pre_delay(self):
        raise NotImplementedError

    # CHORUS_FEEDBACK
    @property
    def chorus_feedback(self):
        return self._read_value('CHORUS_FEEDBACK')

    @chorus_feedback.setter
    def chorus_feedback(self, value):
        return self._write_value('CHORUS_FEEDBACK', value)

    @chorus_feedback.deleter
    def chorus_feedback(self):
        raise NotImplementedError

    # EV_5_PARAM
    @property
    def ev5_param(self):
        return self._read_value('EV_5_PARAM')

    @ev5_param.setter
    def ev5_param(self, value):
        return self._write_value('EV_5_PARAM', value)

    @ev5_param.deleter
    def ev5_param(self):
        raise NotImplementedError

    # EXT_CONTROL_1
    @property
    def ext_control_1(self):
        return self._read_value('EXT_CONTROL_1')

    @ext_control_1.setter
    def ext_control_1(self, value):
        return self._write_value('EXT_CONTROL_1', value)

    @ext_control_1.deleter
    def ext_control_1(self):
        raise NotImplementedError

    # EXT_CONTROL_2
    @property
    def ext_control_2(self):
        return self._read_value('EXT_CONTROL_2')

    @ext_control_2.setter
    def ext_control_2(self, value):
        return self._write_value('EXT_CONTROL_2', value)

    @ext_control_2.deleter
    def ext_control_2(self):
        raise NotImplementedError

    # GROUP
    @property
    def group(self):
        if self._read_value('ADDR_LSB') == 64:
            return 'B'
        else:
            return 'A'

    @group.setter
    def group(self, value):
        if value == 'A':
            group = 0
        elif value == 'B':
            group = 64
        else:
            raise ValueError
        return self._write_value('ADDR_LSB', [group])

    @group.deleter
    def group(self):
        raise NotImplementedError

    @property
    def bank(self):
        if self._read_value('ADDR_MSB') == 0: return 0
        return int((self._read_value('ADDR_MSB') - 64) / 8) + 1

    @bank.setter
    def bank(self, value):
        value = ((value -1) * 7) + self.program + 64
        return self._write_value('ADDR_MSB', value)
    
    @property
    def program(self):
        if self._read_value('ADDR_MSB') == 0: return 0
        return int((self._read_value('ADDR_MSB') - 64) % 8) + 1

    @program.setter
    def program(self, value):
        value = self.bank + value
        return self._write_value('ADDR_MSB', value)

def read_sysex(filename):
    program = []
    try:
        with open(filename, 'rb') as file:
            for x in range(0, 127):
                program.append(RolandGp8(file.read(59)))
    except (FileExistsError, FileNotFoundError):
        exit(' '.join(["Could not open", filename, "for read. Sorry."]))
    return program


program = read_sysex('sysex_to_read.syx')
