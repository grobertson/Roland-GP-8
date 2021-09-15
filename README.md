# Roland GP-8 MIDI library
# 

Implementation of an object which can parse/edit the Roland GP-8's SYSEX patch format.

## But, why? 

LONG discontinued, the Roland GP-8 rackmounted guitar effects processor is a vintage gem. Simply put, the GP-8 is 8 vintage BOSS stomp boxes -- SIX fully analog effects!! -- shoved into a 1U rackmount chassis.

The GP-8 is still (2021) relatively easy find used, has *excellent* analog effects, and IMHO is an insane amount of value in one unit. 

Released in 1987, the GP-8 (And the "New for '89!" all digital GP-16 released in 1989) suffer from one major drawback -- working with all those settings on a 2x16 character LCD using 10 buttons and a rotary encoder is time consuming, error prone, and ultimately very frustrating.

User created software tools for the GP-(8|16) were available, once upon a time. If you spend as much time searching for them as I have, you'll find forum posts from years ago, but no software.

Still a bit of a work in progress, there is enough functionality in the library to parse and edit all of (almost.. TODO: Handle delay time correctly) Roland's sysex binary format for the GP-8. Using something like IPython shell it's now pretty simple to work with the SYSEX records -- However, there is no cli or gui interface yet.

* Using GP-8 implementation to work with ideas about (mostly?) generic definition of SYSEX formats.
* I also have a device, sysex dumps, and the manuals for the GP-8's successor, the GP-16.
* Ultimately, I want to cover both of these vintage effects processors.

### What works?

* Parse recrds from a GP-8 SYSEX dump
* Edit all values of patch settings.
* Toggle effects, set effect parameters.
* Easy properties based access to all values.
* The ./devices/gp8.py module (mostly) 'describes' the SYSEX data format.

### What doesn't work? (yet)

* Device definition module is still a WIP. 
* Using GP-8 implementation to work with ideas about (mostly?) generic definition of SYSEX formats.
* I have a device, sysex dumps, and the manuals for the GP-8's successor, the GP-16.
* Ultimately, I want to cover both of these vintage effects processors.
* No cli or gui tool for editing.
* No midi client. Currently works with exported sysex data in files. (send_midi from the Mididings project works, see my [patched/updated fork of Mididings here](https://github.com/grobertson/mididings).)
