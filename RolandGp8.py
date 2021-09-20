#!/usr/bin/env python3

import binascii
import devices.gp8 as _gp8


class RolandGp8():
    """ Object abstraction for Roland GP-8 program sysex command.
        Refer to GP-8 Notes.md, and the Roland GP-8 Owner's Manual
        for deeper dives.
    """

    def __init__(self, record=None):
        """ If initialized with no params, the object returned is a "blank" record
            with the address set to write to the immediate mode temp area at '00 00' 
        """
        if record == None:
            """ This hex string becomes the baseline for a new patch. All
                effects off, name set to "*Untitled"
            """
            record = binascii.unhexlify(
                b'f041001312000000000050646464643c006432211e003232323c64320310191a0f64411b140000002a556e7469746c656420202020202020200012f7')
        self._record = bytearray(record)
        self._gp8 = _gp8.data
        self._effect_lookup = _gp8.BANK_1_EFFECTS_MSB
        self._effect_lookup.update(_gp8.BANK_2_EFFECTS_LSB)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return ''.join([str(self.group), '-', str(self.bank), '-', str(self.program), ':', self.name])

    def _read_value(self, name):
        """ Read data from the sysex buffer using the data dictionary """
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

    def _reset_value(self, name):
        """Resets the named value to its default as defined in the device data dictionary.

        Args:
            name ([string]): The name of the value from self._gp8 to reset in self._record  
        """
        data = self._gp8[name]
        self._record[data['position']:data['position'] +
                     data['length']] = data['default']

    def _write_value(self, name, value):
        """Write data to the self._record buffer using the data dictionary

        Args:
            name ([string]): The name of the value from self._gp8  
            value ([type]): A value/type appropriate as defined in self._gp8.
        """
        data = self._gp8[name]
        if data['type'] in ['int', 'bitwise'] and type(value) == type(0):
            if value in data['range']:
                self._record[data['position']
                    :data['position'] + data['length']] = [value]
            else:
                raise ValueError

        if data['type'] == 'bool':
            if value:
                self._record[data['position']
                    :data['position'] + data['length']] = [100]
            else:
                self._record[data['position']
                    :data['position'] + data['length']] = [0]

    def _effect_get(self, bank, effect):
        """Read data from the sysex buffer using the data dictionary

        Args:
            bank ([string]): EFFECT_MSB or EFFECT_LSB
            effect ([string]): Effect name in self.

        Returns:
            [bool]: Effect is either on (True) or off (False).
        """
        return bool(self._read_value(bank) & self._effect_lookup[effect] == self._effect_lookup[effect])

    def _effect_set(self, bank, effect, value):
        """ Change data in the sysex buffer using the data dictionary """
        if value != bool(self._read_value(bank) & self._effect_lookup[effect] == self._effect_lookup[effect]):
            # XOR flip the bit
            self._write_value(bank, self._read_value(
                bank) ^ self._effect_lookup[effect])

    def csv_hex(self):
        """ Return the current patch as a hex string that can easily be used with 
            the send_midi utility provided by the mididings package.
        """
        csv = []
        for byte in self._record:
            csv.append(byte.to_bytes(1, 'big').hex())
        return ','.join(csv)

    @property
    def name(self):
        """ Returns the name of the patch as a string """
        data = self._gp8['NAME']
        return self._record[data['position']:data['position'] + data['length']].decode('ascii')

    @name.setter
    def name(self, value):
        """ Update the name of the patch. Automatically padded/trimmed to 16 chars """
        data = self._gp8['NAME']
        while len(value) <= data['length']:
            """Pad the string to length with spaces"""
            value = value + " "
        self._record[data['position']:data['position'] +
                     data['length']] = bytes(value, 'ascii')

    @name.deleter
    def name(self):
        """ Reset the patch name to a default value as defined in the data dictionary. """
        self._reset_value('NAME')

    @property
    def volume(self):
        """ Return the master volume as int 0-100 """
        return self._read_value('MASTER_VOLUME')

    @volume.setter
    def volume(self, value):
        return self._write_value('MASTER_VOLUME', value)

    @volume.deleter
    def volume(self):
        return self._reset_value('MASTER_VOLUME')

    # EFFECT BIT SWITCHES

    # Dynamic Filter
    @property
    def filter(self):
        """True if the effect is on.

        Returns:
            [bool]: Effect is either on or off
        """
        return self._effect_get('EFFECT_LSB', 'DYNAMIC_FILTER')

    @filter.setter
    def filter(self, value):
        self._effect_set('EFFECT_LSB', 'DYNAMIC_FILTER', value)

    @filter.deleter
    def filter(self):
        return self._reset_value('DYNAMIC_FILTER')

    # Compressor
    @property
    def compressor(self):
        """True if the effect is on.

        Returns:
            [bool]: Effect is either on or off
        """
        return self._effect_get('EFFECT_LSB', 'COMPRESSOR')

    @compressor.setter
    def compressor(self, value):
        self._effect_set('EFFECT_LSB', 'COMPRESSOR', value)

    @compressor.deleter
    def compressor(self):
        return self._reset_value('COMPRESSOR')

    # Overdrive
    @property
    def overdrive(self):
        """True if the effect is on.

        Returns:
            [bool]: Effect is either on or off
        """
        return self._effect_get('EFFECT_LSB', 'OVERDRIVE')

    @overdrive.setter
    def overdrive(self, value):
        self._effect_set('EFFECT_LSB', 'OVERDRIVE', value)

    @overdrive.deleter
    def overdrive(self):
        return self._reset_value('OVERDRIVE')

    # Distortion
    @property
    def distortion(self):
        """True if the effect is on.

        Returns:
            [bool]: Effect is either on or off
        """
        return self._effect_get('EFFECT_LSB', 'DISTORTION')

    @distortion.setter
    def distortion(self, value):
        self._effect_set('EFFECT_LSB', 'DISTORTION', value)

    @distortion.deleter
    def distortion(self):
        return self._reset_value('DISTORTION')

    # Phaser
    @property
    def phaser(self):
        """True if the effect is on.

        Returns:
            [bool]: Effect is either on or off
        """
        return self._effect_get('EFFECT_MSB', 'PHASER')

    @phaser.setter
    def phaser(self, value):
        self._effect_set('EFFECT_MSB', 'PHASER', value)

    @phaser.deleter
    def phaser(self):
        return self._reset_value('PHASER')

    # Equalizer
    @property
    def equalizer(self):
        """True if the effect is on.

        Returns:
            [bool]: Effect is either on or off
        """
        return self._effect_get('EFFECT_MSB', 'EQUALIZER')

    @equalizer.setter
    def equalizer(self, value):
        self._effect_set('EFFECT_MSB', 'EQUALIZER', value)

    @equalizer.deleter
    def equalizer(self):
        return self._reset_value('EQUALIZER')

    # Delay
    @property
    def delay(self):
        """True if the effect is on.

        Returns:
            [bool]: Effect is either on or off
        """
        return self._effect_get('EFFECT_MSB', 'DELAY')

    @delay.setter
    def delay(self, value):
        self._effect_set('EFFECT_MSB', 'DELAY', value)

    @delay.deleter
    def delay(self):
        return self._reset_value('DELAY')

    # Chorus
    @property
    def chorus(self):
        """True if the effect is on.

        Returns:
            [bool]: Effect is either on or off
        """
        return self._effect_get('EFFECT_MSB', 'CHORUS')

    @chorus.setter
    def chorus(self, value):
        self._effect_set('EFFECT_MSB', 'CHORUS', value)

    @chorus.deleter
    def chorus(self):
        return self._reset_value('CHORUS')

    # For convenience
    @property
    def effects(self):
        """A convenience function which returns the on/off status of all available effects.

        Returns:
            [dict]: A dictionary with effect names as keys, and bool values for each.
        """
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
    # Effect Properties
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
        self._reset_value('FILTER_SENS')

    # FILTER_CUTOFF_FREQ
    @property
    def filter_cutoff_freq(self):
        return self._read_value('FILTER_CUTOFF_FREQ')

    @filter_cutoff_freq.setter
    def filter_cutoff_freq(self, value):
        return self._write_value('FILTER_CUTOFF_FREQ', value)

    @filter_cutoff_freq.deleter
    def filter_cutoff_freq(self):
        self._reset_value('FILTER_CUTOFF_FREQ')

    # FILTER_Q
    @property
    def filter_q(self):
        return self._read_value('FILTER_Q')

    @filter_q.setter
    def filter_q(self, value):
        return self._write_value('FILTER_Q', value)

    @filter_q.deleter
    def filter_q(self):
        self._reset_value('FILTER_Q')

    # FILTER_UP_DOWN
    @property
    def filter_up_down(self):
        return self._read_value('FILTER_UP_DOWN')

    @filter_up_down.setter
    def filter_up_down(self, value):
        return self._write_value('FILTER_UP_DOWN', value)

    @filter_up_down.deleter
    def filter_up_down(self):
        self._reset_value('FILTER_UP_DOWN')

    # COMP_ATTACK
    @property
    def comp_attack(self):
        return self._read_value('COMP_ATTACK')

    @comp_attack.setter
    def comp_attack(self, value):
        return self._write_value('COMP_ATTACK', value)

    @comp_attack.deleter
    def comp_attack(self):
        self._reset_value('COMP_ATTACK')

    # COMP_SUSTAIN
    @property
    def comp_sustain(self):
        return self._read_value('COMP_SUSTAIN')

    @comp_sustain.setter
    def comp_sustain(self, value):
        return self._write_value('COMP_SUSTAIN', value)

    @comp_sustain.deleter
    def comp_sustain(self):
        self._reset_value('COMP_SUSTAIN')

    # OD_TONE
    @property
    def od_tone(self):
        return self._read_value('OD_TONE')

    @od_tone.setter
    def od_tone(self, value):
        return self._write_value('OD_TONE', value)

    @od_tone.deleter
    def od_tone(self):
        self._reset_value('OD_TONE')

    # OD_DRIVE
    @property
    def od_drive(self):
        return self._read_value('OD_DRIVE')

    @od_drive.setter
    def od_drive(self, value):
        return self._write_value('OD_DRIVE', value)

    @od_drive.deleter
    def od_drive(self):
        self._reset_value('OD_DRIVE')

    # OD_TURBO
    @property
    def od_turbo(self):
        return self._read_value('OD_TURBO')

    @od_turbo.setter
    def od_turbo(self, value):
        return self._write_value('OD_TURBO', value)

    @od_turbo.deleter
    def od_turbo(self):
        self._reset_value('OD_TURBO')

    # DIST_TONE
    @property
    def dist_tone(self):
        return self._read_value('DIST_TONE')

    @dist_tone.setter
    def dist_tone(self, value):
        return self._write_value('DIST_TONE', value)

    @dist_tone.deleter
    def dist_tone(self):
        self._reset_value('DIST_TONE')

    # DIST_DIST
    @property
    def dist_dist(self):
        return self._read_value('DIST_DIST')

    @dist_dist.setter
    def dist_dist(self, value):
        return self._write_value('DIST_DIST', value)

    @dist_dist.deleter
    def dist_dist(self):
        self._reset_value('DIST_DIST')

    # PHASER_RATE
    @property
    def phaser_rate(self):
        return self._read_value('PHASER_RATE')

    @phaser_rate.setter
    def phaser_rate(self, value):
        return self._write_value('PHASER_RATE', value)

    @phaser_rate.deleter
    def phaser_rate(self):
        self._reset_value('PHASER_RATE')

    # PHASER_DEPTH
    @property
    def phaser_depth(self):
        return self._read_value('PHASER_DEPTH')

    @phaser_depth.setter
    def phaser_depth(self, value):
        return self._write_value('PHASER_DEPTH', value)

    @phaser_depth.deleter
    def phaser_depth(self):
        self._reset_value('PHASER_DEPTH')

    # PHASER_RESONANCE
    @property
    def phaser_resonance(self):
        return self._read_value('PHASER_RESONANCE')

    @phaser_resonance.setter
    def phaser_resonance(self, value):
        return self._write_value('PHASER_RESONANCE', value)

    @phaser_resonance.deleter
    def phaser_resonance(self):
        self._reset_value('PHASER_RESONANCE')

    # EQ_HI
    @property
    def eq_hi(self):
        return self._read_value('EQ_HI')

    @eq_hi.setter
    def eq_hi(self, value):
        return self._write_value('EQ_HI', value)

    @eq_hi.deleter
    def eq_hi(self):
        self._reset_value('EQ_HI')

    # EQ_MID
    @property
    def eq_mid(self):
        return self._read_value('EQ_MID')

    @eq_mid.setter
    def eq_mid(self, value):
        return self._write_value('EQ_MID', value)

    @eq_mid.deleter
    def eq_mid(self):
        self._reset_value('EQ_MID')

    # EQ_LO
    @property
    def eq_lo(self):
        return self._read_value('EQ_LO')

    @eq_lo.setter
    def eq_lo(self, value):
        return self._write_value('EQ_LO', value)

    @eq_lo.deleter
    def eq_lo(self):
        self._reset_value('EQ_LO')

    # EQ_GAIN
    @property
    def eq_gain(self):
        return self._read_value('EQ_GAIN')

    @eq_gain.setter
    def eq_gain(self, value):
        return self._write_value('EQ_GAIN', value)

    @eq_gain.deleter
    def eq_gain(self):
        self._reset_value('EQ_GAIN')

    # DELAY_LEVEL
    @property
    def delay_level(self):
        return self._read_value('DELAY_LEVEL')

    @delay_level.setter
    def delay_level(self, value):
        return self._write_value('DELAY_LEVEL', value)

    @delay_level.deleter
    def delay_level(self):
        self._reset_value('DELAY_LEVEL')

    # DELAY_FEEDBACK
    @property
    def delay_feedback(self):
        return self._read_value('DELAY_FEEDBACK')

    @delay_feedback.setter
    def delay_feedback(self, value):
        return self._write_value('DELAY_FEEDBACK', value)

    @delay_feedback.deleter
    def delay_feedback(self):
        self._reset_value('DELAY_FEEDBACK')

    # CHORUS_RATE
    @property
    def chorus_rate(self):
        return self._read_value('CHORUS_RATE')

    @chorus_rate.setter
    def chorus_rate(self, value):
        return self._write_value('CHORUS_RATE', value)

    @chorus_rate.deleter
    def chorus_rate(self):
        self._reset_value('CHORUS_RATE')

    # CHORUS_DEPTH
    @property
    def chorus_depth(self):
        return self._read_value('CHORUS_DEPTH')

    @chorus_depth.setter
    def chorus_depth(self, value):
        return self._write_value('CHORUS_DEPTH', value)

    @chorus_depth.deleter
    def chorus_depth(self):
        self._reset_value('CHORUS_DEPTH')

    # CHORUS_LEVEL
    @property
    def chorus_level(self):
        return self._read_value('CHORUS_LEVEL')

    @chorus_level.setter
    def chorus_level(self, value):
        return self._write_value('CHORUS_LEVEL', value)

    @chorus_level.deleter
    def chorus_level(self):
        self._reset_value('CHORUS_LEVEL')

    # CHORUS_PRE_DELAY
    @property
    def chorus_pre_delay(self):
        return self._read_value('CHORUS_PRE_DELAY')

    @chorus_pre_delay.setter
    def chorus_pre_delay(self, value):
        return self._write_value('CHORUS_PRE_DELAY', value)

    @chorus_pre_delay.deleter
    def chorus_pre_delay(self):
        self._reset_value('CHORUS_PRE_DELAY')

    # CHORUS_FEEDBACK
    @property
    def chorus_feedback(self):
        return self._read_value('CHORUS_FEEDBACK')

    @chorus_feedback.setter
    def chorus_feedback(self, value):
        return self._write_value('CHORUS_FEEDBACK', value)

    @chorus_feedback.deleter
    def chorus_feedback(self):
        self._reset_value('CHORUS_FEEDBACK')

    # EV_5_PARAM
    @property
    def ev5_param(self):
        return self._read_value('EV_5_PARAM')

    @ev5_param.setter
    def ev5_param(self, value):
        return self._write_value('EV_5_PARAM', value)

    @ev5_param.deleter
    def ev5_param(self):
        self._reset_value('EV_5_PARAM')

    # EXT_CONTROL_1
    @property
    def ext_control_1(self):
        return self._read_value('EXT_CONTROL_1')

    @ext_control_1.setter
    def ext_control_1(self, value):
        return self._write_value('EXT_CONTROL_1', value)

    @ext_control_1.deleter
    def ext_control_1(self):
        self._reset_value('EXT_CONTROL_1')

    # EXT_CONTROL_2
    @property
    def ext_control_2(self):
        return self._read_value('EXT_CONTROL_2')

    @ext_control_2.setter
    def ext_control_2(self, value):
        return self._write_value('EXT_CONTROL_2', value)

    @ext_control_2.deleter
    def ext_control_2(self):
        self._reset_value('EXT_CONTROL_2')

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

    @property
    def bank(self):
        if self._read_value('ADDR_MSB') == 0:
            return 0
        return int((self._read_value('ADDR_MSB') - 64) / 8) + 1

    @bank.setter
    def bank(self, value):
        value = ((value - 1) * 7) + self.program + 64
        return self._write_value('ADDR_MSB', value)

    @property
    def program(self):
        if self._read_value('ADDR_MSB') == 0:
            return 0
        return int((self._read_value('ADDR_MSB') - 64) % 8) + 1

    @program.setter
    def program(self, value):
        value = self.bank + value
        return self._write_value('ADDR_MSB', value)


