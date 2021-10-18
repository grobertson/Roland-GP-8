import unittest
from RolandGp8 import RolandGp8

class TestRolandGp8(unittest.TestCase):

    def setUp(self):
        self.p = RolandGp8()

    def effect_test_by_name(self, effect):
        '''Doesn't fit well into generics'''
        name = effect.lower()
        default_val = False
        self.assertEqual(int(self.p.__getattribute__(name)), default_val)
        self.p.__setattr__(name, True)
        self.assertEqual(int(self.p.__getattribute__(name)), True)
        self.p.__setattr__(name, False)
        self.assertEqual(int(self.p.__getattribute__(name)), False)

    def generic_test_by_prop_id(self, property_key):
        property_name = property_key.lower()
        data = self.p._gp8[property_key]
        default_val = data['default']
        val_range = data['range']
        max_val = max(val_range)
        min_val = min(val_range)
        #test read
        self.assertEqual(int(self.p.__getattribute__(property_name)), default_val)
        #write
        self.p.__setattr__(property_name, max_val)
        self.assertEqual(self.p.__getattribute__(property_name), max_val)
        self.p.__setattr__(property_name, min_val)
        self.assertEqual(self.p.__getattribute__(property_name), min_val)
        #out of range
        if data['type'] != 'bool':
            # boolean is represented as either nothing or true, so "max +1" isn't useful
            with self.assertRaises(ValueError):
                #set out of range value
                self.p.__setattr__(property_name, max_val + 1)
            with self.assertRaises(ValueError):
                #set out of range value
                self.p.__setattr__(property_name, min_val - 1)
        #reset
        self.p.__delattr__(property_name)
        self.assertEqual(self.p.__getattribute__(property_name), default_val)

    def test_property_name_new(self):
        ''' New object has correct default name '''
        #Initial/Default
        #New record = '*Untitled' padded to 16
        self.assertEqual(self.p.name, '*Untitled       ')

    def test_property_name_set(self):
        ''' Set name via property '''
        #Set name (exactly 16)
        self.p.name = 'This is 16 chars'
        self.assertEqual(self.p.name, 'This is 16 chars')

    def test_property_name_set_too_short(self):
        ''' Padding added when name property set to a value shorter than expected'''
        #Too short
        self.p.name = 'This is 16'
        self.assertEqual(self.p.name, 'This is 16      ')

    def test_property_name_set_too_long(self):
        ''' String trimmed to length when name property set to value longer than expected '''
        #Too long
        self.p.name = 'This is 16 chars plus a few too many'
        self.assertEqual(self.p.name, 'This is 16 chars')

    def test_property_name_reset(self):
        ''' Deleting the property resets it to the default value '''
        #Set and Reset it
        self.p.name = 'This is 16'
        del(self.p.name)
        self.assertEqual(self.p.name, '*Untitled       ')

    def test_property_bank(self):
        '''Test property _ '''
        pass

    def test_property_group(self):
        '''Test property GROUP '''
        #self.generic_test_by_prop_id('GROUP')
        pass

    def test_property_program(self):
        '''Test property PROGRAM '''
        #self.generic_test_by_prop_id('PROGRAM')
        pass

    def test_export_csv_hex(self):
        '''Test property _ '''
        pass

    def test_property_filter(self):
        '''Test property FILTER '''
        self.effect_test_by_name('filter')

    def test_property_overdrive(self):
        '''Test property OVERDRIVE '''
        self.effect_test_by_name('overdrive')


    def test_property_dist_tone(self):
        '''Test property DIST_TONE '''
        self.generic_test_by_prop_id('DIST_TONE')

    def test_property_eq_lo(self):
        '''Test property EQ_LO '''
        self.generic_test_by_prop_id('EQ_LO')

    def test_property_ext_control_2(self):
        '''Test property EXT_CONTROL_2 '''
        self.generic_test_by_prop_id('EXT_CONTROL_2')

    def test_property_filter_up_down(self):
        '''Test property FILTER_UP_DOWN '''
        self.generic_test_by_prop_id('FILTER_UP_DOWN')

    def test_property_od_turbo(self):
        '''Test property OD_TURBO '''
        self.generic_test_by_prop_id('OD_TURBO')

    def test_property_phaser_resonance(self):
        '''Test property PHASER_RESONANCE '''
        self.generic_test_by_prop_id('PHASER_RESONANCE')

    def test_property_chorus(self):
        '''Test property CHORUS '''
        self.effect_test_by_name('CHORUS')
    
    def test_property_chorus_pre_delay(self):
        '''Test property CHORUS_PRE_DELAY '''
        self.generic_test_by_prop_id('CHORUS_PRE_DELAY')

    def test_property_chorus_rate(self):
        '''Test property CHORUS_RATE '''
        self.generic_test_by_prop_id('CHORUS_RATE')

    def test_property_delay(self):
        '''Test property DELAY '''
        self.effect_test_by_name('delay')

    def test_property_distortion(self):
        '''Test property DISTORTION '''
        self.effect_test_by_name('distortion')

    def test_property_eq_mid(self):
        '''Test property EQ_MID '''
        self.generic_test_by_prop_id('EQ_MID')

    def test_property_chorus_depth(self):
        '''Test property CHORUS_DEPTH '''
        self.generic_test_by_prop_id('CHORUS_DEPTH')

    def test_property_comp_attack(self):
        '''Test property COMP_ATTACK '''
        self.generic_test_by_prop_id('COMP_ATTACK')

    def test_property_delay_feedback(self):
        '''Test property DELAY_FEEDBACK '''
        self.generic_test_by_prop_id('DELAY_FEEDBACK')

    def test_property_effects(self):
        '''Test property EFFECTS '''
        pass

    def test_property_equalizer(self):
        '''Test property EQUALIZER '''
        self.effect_test_by_name('EQUALIZER')

    def test_property_filter_cutoff_freq(self):
        '''Test property FILTER_CUTOFF_FREQ '''
        self.generic_test_by_prop_id('FILTER_CUTOFF_FREQ')

    def test_property_phaser(self):
        '''Test property PHASER '''
        self.effect_test_by_name('phaser')

    def test_property_chorus_feedback(self):
        '''Test property CHORUS_FEEDBACK '''
        self.generic_test_by_prop_id('CHORUS_FEEDBACK')

    def test_property_comp_sustain(self):
        '''Test property COMP_SUSTAIN '''
        self.generic_test_by_prop_id('COMP_SUSTAIN')

    def test_property_delay_level(self):
        '''Test property DELAY_LEVEL '''
        self.generic_test_by_prop_id('DELAY_LEVEL')

    def test_property_eq_gain(self):
        '''Test property EQ_GAIN '''
        self.generic_test_by_prop_id('EQ_GAIN')

    def test_property_ev5_param(self):
        '''Test property EV5_PARAM '''
        self.generic_test_by_prop_id('EV5_PARAM')

    def test_property_filter_q(self):
        '''Test property FILTER_Q '''
        self.generic_test_by_prop_id('FILTER_Q')

    def test_property_od_drive(self):
        '''Test property OD_DRIVE '''
        self.generic_test_by_prop_id('OD_DRIVE')

    def test_property_phaser_depth(self):
        '''Test property PHASER_DEPTH '''
        self.generic_test_by_prop_id('PHASER_DEPTH')

    def test_property_volume(self):
        '''Test property VOLUME '''
        self.generic_test_by_prop_id('VOLUME')

    def test_property_chorus_level(self):
        '''Test property CHORUS_LEVEL '''
        self.generic_test_by_prop_id('CHORUS_LEVEL')

    def test_property_compressor(self):
        '''Test property COMPRESSOR '''
        self.effect_test_by_name('compressor')

    def test_property_dist_dist(self):
        '''Test property DIST_DIST '''
        self.generic_test_by_prop_id('DIST_DIST')

    def test_property_eq_hi(self):
        '''Test property EQ_HI '''
        self.generic_test_by_prop_id('EQ_HI')

    def test_property_ext_control_1(self):
        '''Test property EXT_CONTROL_1 '''
        self.generic_test_by_prop_id('EXT_CONTROL_1')

    def test_property_filter_sens(self):
        '''Test property FILTER_SENS '''
        self.generic_test_by_prop_id('FILTER_SENS')

    def test_property_od_tone(self):
        '''Test property OD_TONE '''
        self.generic_test_by_prop_id('OD_TONE')

    def test_property_phaser_rate(self):
        '''Test property PHASER_RATE '''
        self.generic_test_by_prop_id('PHASER_RATE')


if __name__ == '__main__':
    unittest.main()


