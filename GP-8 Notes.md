


                                st|mf|id|md|op|ms|ls|Data    |ck,ex                                                                                        
send_midi -A USB\ Midi\.* SYSEX,F0,41,03,13,12,40,00,nn,nn...,FF,F7


Construction of Roland GP Sysex messages
---

An example Sys Ex packet.

st|mf|id|md|op|ms|ls|Data    |ck,ex                                                                                        
F0,41,01,13,12,40,00,nn,nn...,FF,F7

st = Start Exclusive message

mf = Manufacturer
        * Roland / BOSS is always 41

id = Device ID. 
        Same as the Midi channel, BUT always zero index. 
        * For the GP-8 Omni ON/OFF appears to have no effect here, device doesn't respond unless equal to current channel.

md = Model ID.
        * GP-8 = 13

op = Operation/Command 
        * 12 = Data Load.
        * 11 = Request Data.

ms = MSB Most Significant Byte - Address
        *   in this case works out to be the starting pointer to the prog number 40 - 7F

ls = LSB Least Significant Byte - Address
        * For GP-8 00 = Group A, 40 = Group Bit

DATA = See reverse engineered examples below

ck = Checksum. Sometimes ignored.
        * "The sum of all bytes after [op] to the end of data"
        * This is easier said as sum of data + LSB + MSB.
        * GP-16 Manual says ignored?
        * GP-8 Manual states checksum is not used when sending 12h (Data Set)

ex = EoX, End of exclusive message

Data for "Dig Chorus"
                       |                       |                       |              |MV|EV|X1|X2|Text Name                                      |Null ends text
08,02,00,50,64,64,64,64,3C,00,64,32,3C,1E,3C,3C,32,32,3C,64,32,02,2C,0F,37,19,64,0E,32,0A,00,00,00,20,44,69,67,20,43,68,6F,72,75,73,20,20,20,20,20,00

X-Ref to address mapping of parameters.
00,01,02,03,04,05,06,07,08,09,0A,0B,0C,0D,0E,0F,10,11,12,13,14,15,16,17,18,19,1A,1B,1C,1D,1E,1F,20,21,22,23,24,25,26,27,28,29,2A,2B,2C,2D,2E,2F,30,31