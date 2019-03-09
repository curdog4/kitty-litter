#!/usr/bin/env python -u
#

import os,sys
import time
from optparse import OptionParser
import picamera

sys.stdout = os.fdopen(sys.stdout.fileno(),'w',0)

class Morse:

    def __init__(self,base_interval=0.1):
        dit = 1 * base_interval
        dah = 3 * base_interval
        self.dit = dit
        self.dah = dah
        self.inter_symbol = 1 * dit
        self.inter_character = 3 * dit
        self.inter_word = 7 * dit
        self.dit_symbol = '.'
        self.dah_symbol = '-'

        self.character_map = {
            'A' : [ dit, dah ],
            'B' : [ dah, dit, dit, dit ],
            'C' : [ dah, dit, dah, dit ],
            'D' : [ dah, dit, dit ],
            'E' : [ dit ],
            'F' : [ dit, dit, dah, dit ],
            'G' : [ dah, dah, dit ],
            'H' : [ dit, dit, dit, dit ],
            'I' : [ dit, dit ],
            'J' : [ dit, dah, dah, dah ],
            'K' : [ dah, dit, dah ],
            'L' : [ dit, dah, dit, dit ],
            'M' : [ dah, dah ],
            'N' : [ dah, dit ],
            'O' : [ dah, dah, dah ],
            'P' : [ dit, dah, dah, dit ],
            'Q' : [ dah, dah, dit, dah ],
            'R' : [ dit, dah, dit ],
            'S' : [ dit, dit, dit ],
            'T' : [ dah ],
            'U' : [ dit, dit, dah ],
            'V' : [ dit, dit, dit, dah ],
            'W' : [ dit, dah, dah ],
            'X' : [ dah, dit, dit, dah ],
            'Y' : [ dah, dit, dah, dah ],
            'Z' : [ dah, dah, dit, dit ],
            '0' : [ dah, dah, dah, dah, dah ],
            '1' : [ dit, dah, dah, dah, dah ],
            '2' : [ dit, dit, dah, dah, dah ],
            '3' : [ dit, dit, dit, dah, dah ],
            '4' : [ dit, dit, dit, dit, dah ],
            '5' : [ dit, dit, dit, dit, dit ],
            '6' : [ dah, dit, dit, dit, dit ],
            '7' : [ dah, dah, dit, dit, dit ],
            '8' : [ dah, dah, dah, dit, dit ],
            '9' : [ dah, dah, dah, dah, dit ],
            '.' : [ dit, dah, dit, dah, dit, dah ],
            ',' : [ dah, dah, dit, dit, dah, dah ],
            ':' : [ dah, dah, dah, dit, dit, dit ],
            '?' : [ dit, dit, dah, dah, dit, dit ],
            '\'': [ dit, dah, dah, dah, dah, dit ],
            '-' : [ dah, dit, dit, dit, dit, dah ],
            '/' : [ dah, dit, dit, dah, dit ],
            '(' : [ dah, dit, dah, dah, dit, dah ],
            '{' : [ dah, dit, dah, dah, dit, dah ],
            '<' : [ dah, dit, dah, dah, dit, dah ],
            '[' : [ dah, dit, dah, dah, dit, dah ],
            ']' : [ dah, dit, dah, dah, dit, dah ],
            '>' : [ dah, dit, dah, dah, dit, dah ],
            '}' : [ dah, dit, dah, dah, dit, dah ],
            ')' : [ dah, dit, dah, dah, dit, dah ],
            '@' : [ dit, dah, dah, dit, dah, dit ],
            '=' : [ dah, dit, dit, dit, dah ]
        }
        self.camera = picamera.PiCamera()
        self.camera.led = False
        time.sleep(self.inter_word)
        return None

    def render(self,mesg):
        for word in mesg.split():
            for i in range(0,len(word)):
                char = word[i]
                m = self.character_map.get(char.upper())
                sys.stdout.write('%s: ' % (char.upper()))
                for s in m:
                    self.camera.led = True
                    if s == self.dit:
                        sys.stdout.write('%s' % (self.dit_symbol))
                        time.sleep(self.dit)
                    elif s == self.dah:
                        sys.stdout.write('%s' % (self.dah_symbol))
                        time.sleep(self.dah)
                    else:
                        sys.stderr.write("\nERROR: Inter-character insanity. What do I do with '%s'?\n" % (s))
                    self.camera.led = False
                    time.sleep(self.inter_symbol)
                time.sleep(self.inter_character)
                sys.stdout.write("\n")
            time.sleep(self.inter_word)
            sys.stdout.write("\n")

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option('-m', '--message', dest='message',
                      default="Hello World", type='string',
                      help="Message to render in morse code")
    parser.add_option('-t', '--base-interval', dest='base_interval',
                      default=0.1, type='float',
                      help="Base time interval (length of 'dit' and inter-symbol spacing)")
    (opts,args) = parser.parse_args()
    m = Morse(base_interval=opts.base_interval)
    m.render(opts.message)
